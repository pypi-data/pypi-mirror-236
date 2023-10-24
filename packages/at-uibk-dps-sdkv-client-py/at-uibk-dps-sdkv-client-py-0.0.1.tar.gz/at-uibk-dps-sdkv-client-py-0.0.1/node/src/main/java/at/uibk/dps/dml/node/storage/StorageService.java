package at.uibk.dps.dml.node.storage;

import at.uibk.dps.dml.client.storage.Flag;
import at.uibk.dps.dml.node.util.Timestamp;
import at.uibk.dps.dml.node.exception.*;
import at.uibk.dps.dml.node.metadata.KeyMetadata;
import at.uibk.dps.dml.node.metadata.MetadataChangeListener;
import at.uibk.dps.dml.node.metadata.MetadataService;
import at.uibk.dps.dml.node.storage.command.*;
import at.uibk.dps.dml.node.storage.rpc.StorageRpcErrorType;
import at.uibk.dps.dml.node.storage.rpc.StorageRpcService;
import at.uibk.dps.dml.node.util.ValidatorChain;
import io.vertx.core.CompositeFuture;
import io.vertx.core.Future;
import io.vertx.core.Promise;
import io.vertx.core.Vertx;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.*;

public class StorageService implements CommandHandler {

    private final Logger logger = LoggerFactory.getLogger(StorageService.class);

    private final Vertx vertx;

    private final int verticleId;

    private final SharedObjectFactory sharedObjectFactory;

    private final StorageRpcService storageRpcService;

    private final MetadataService metadataService;

    private final Map<String, StorageObject> objects = new HashMap<>();

    private int requestCounter = 0;

    // Maps keys to pending commands
    private final Map<String, Queue<PendingCommand>> pendingCommands = new HashMap<>();

    public StorageService(Vertx vertx, int verticleId, SharedObjectFactory sharedObjectFactory,
                          StorageRpcService storageRpcService, MetadataService metadataService) {
        this.vertx = vertx;
        this.verticleId = verticleId;
        this.sharedObjectFactory = sharedObjectFactory;
        this.storageRpcService = storageRpcService;
        this.metadataService = metadataService;
        metadataService.setListener(new MetadataChangeListener() {
            @Override
            public Future<Void> keyInvalidated(String key, KeyMetadata oldMetadata, KeyMetadata newMetadata) {
                return onMetadataServiceKeyInvalidated(key, oldMetadata, newMetadata);
            }

            @Override
            public void keyValidated(String key, KeyMetadata metadata) {
                onMetadataServiceKeyValidated(key, metadata);
            }
        });
    }

    @SuppressWarnings({"rawtypes", "unchecked"})
    public Future<Integer> lock(String key) {
        Promise promise = Promise.promise();
        LockCommand command = new LockCommand(promise, key, null, verticleId);
        enqueueCommand(command);
        return promise.future();
    }

    @SuppressWarnings({"rawtypes", "unchecked"})
    public Future<Void> unlock(String key, int lockToken) {
        Promise promise = Promise.promise();
        enqueueCommand(new UnlockCommand(promise, key, lockToken, verticleId));
        return promise.future();
    }

    @SuppressWarnings({"rawtypes", "unchecked"})
    public Future<Void> initObject(String key, String languageId, String objectType, byte[] encodedArgs,
                                   Integer lockToken) {
        Promise promise = Promise.promise();
        enqueueCommand(new InitObjectCommand(promise, key, lockToken, verticleId, languageId, objectType, encodedArgs));
        return promise.future();
    }

    @SuppressWarnings({"rawtypes", "unchecked"})
    public Future<byte[]> invokeMethod(String key, String methodName, byte[] encodedArgs,
                                       Integer lockToken, Set<Flag> flags) {
        Promise promise = Promise.promise();
        enqueueCommand(new InvokeMethodCommand(promise, key, lockToken, flags.contains(Flag.READ_ONLY),
                flags.contains(Flag.ALLOW_INVALID_READS), verticleId, flags.contains(Flag.ASYNC_REPLICATION),
                methodName, encodedArgs));
        return promise.future();
    }

    public Future<Void> invalidate(int originVerticleId, Timestamp timestamp, InvalidationCommand command) {
        StorageObject storageObject = objects.get(command.getKey());
        Optional<Throwable> error = new ValidatorChain<Throwable>()
                .validate(() -> checkObjectExists(storageObject))
                .validate(() -> checkOriginIsPrimaryReplicaOfKey(command.getKey(), originVerticleId))
                .validate(() -> checkObjectIsReady(storageObject)).getError();
        if (error.isPresent()) return Future.failedFuture(error.get());

        Timestamp localTimestamp = storageObject.getTimestamp();

        // Conflicting timestamps can occur if we have at least three replicas and the primary replica crashes during
        // a write operation
        boolean conflictingTimestamps = timestamp.getCoordinatorVerticleId() != localTimestamp.getCoordinatorVerticleId()
                && storageObject.getState() != StorageObjectState.VALID;

        boolean timestampIsNextInSequence = timestamp.getVersion() == localTimestamp.getVersion() + 1 && !conflictingTimestamps;

        // We can apply the command if the timestamp is the next in the sequence or if the command
        // overwrites the whole state of the object with a newer version
        boolean canApplyCommand = timestampIsNextInSequence || (command instanceof StateReplicationCommand
                && (conflictingTimestamps || timestamp.getVersion() > localTimestamp.getVersion()));

        if (!canApplyCommand) {
            if (conflictingTimestamps) {
                return Future.failedFuture(new ConflictingTimestampsException());
            }
            if (timestamp.getVersion() - localTimestamp.getVersion() > 1) {
                return Future.failedFuture(new MissingMessagesException());
            }
            if (timestamp.getVersion() <= localTimestamp.getVersion()) {
                // We already received this command, we simply ACK it
                return Future.succeededFuture();
            }
            return Future.failedFuture(new CommandRejectedException());
        }

        storageObject.setState(StorageObjectState.INVALID);
        localTimestamp.setVersion(timestamp.getVersion());
        localTimestamp.setCoordinatorVerticleId(timestamp.getCoordinatorVerticleId());

        try {
            command.apply(this);
        } catch (Exception e) {
            logger.debug("Error while applying invalidation command", e);
        }
        return Future.succeededFuture();
    }

    public Future<Void> commit(int originVerticleId, String key, Timestamp timestamp) {
        StorageObject storageObject = objects.get(key);
        Optional<Throwable> error = new ValidatorChain<Throwable>()
                .validate(() -> checkObjectExists(storageObject))
                .validate(() -> checkOriginIsPrimaryReplicaOfKey(key, originVerticleId))
                .validate(() -> checkObjectIsReady(storageObject))
                .getError();
        if (error.isPresent()) return Future.failedFuture(error.get());

        if (timestamp.equals(storageObject.getTimestamp())) {
            storageObject.setState(StorageObjectState.VALID);
            handlePendingCommandsAsync(key);
        }

        return Future.succeededFuture();
    }

    public Future<StorageObject> getObject(String key) {
        StorageObject storageObject = objects.get(key);
        Optional<Throwable> error = new ValidatorChain<Throwable>()
                .validate(() -> checkObjectExists(storageObject))
                .validate(() -> checkObjectIsReady(storageObject))
                .getError();
        //noinspection OptionalIsPresent
        if (error.isPresent()) return Future.failedFuture(error.get());

        return Future.succeededFuture(storageObject);
    }

    @Override
    public Object apply(StateReplicationCommand command) {
        objects.get(command.getKey()).copyFrom(command.getStorageObject());
        return null;
    }

    @Override
    public Object apply(LockCommand command) {
        StorageObject storageObject = objects.get(command.getKey());
        storageObject.setLocked(true);
        storageObject.setLockToken(storageObject.getLockToken() + 1);
        return storageObject.getLockToken();
    }

    @Override
    public Object apply(UnlockCommand command) {
        StorageObject storageObject = objects.get(command.getKey());
        storageObject.setLocked(false);
        return null;
    }

    @Override
    public Object apply(InitObjectCommand command) {
        StorageObject storageObject = objects.get(command.getKey());
        storageObject.setSharedObject(sharedObjectFactory.createObject(
                command.getLanguageId(), command.getObjectType(), command.getEncodedArgs()));
        return null;
    }

    @Override
    public Object apply(InvokeMethodCommand command) {
        StorageObject storageObject = objects.get(command.getKey());
        SharedObject sharedObject = storageObject.getSharedObject();
        if (sharedObject == null) {
            throw new ObjectNotInitializedException();
        }
        return sharedObject.invokeMethod(command.getMethodName(), command.getEncodedArgs());
    }

    private void enqueueCommand(Command command) {
        StorageObject storageObject = objects.get(command.getKey());
        Optional<Throwable> error = new ValidatorChain<Throwable>()
                .validate(() -> checkObjectExists(storageObject))
                .getError();
        if (error.isPresent()) {
            command.getPromise().fail(error.get());
            return;
        }

        Queue<PendingCommand> queue = pendingCommands.computeIfAbsent(command.getKey(), k -> new PriorityQueue<>());
        queue.add(new PendingCommand(command, requestCounter++));
        handlePendingCommands(command.getKey());
    }

    private void handlePendingCommands(String key) {
        StorageObject storageObject = objects.get(key);
        if (storageObject == null) {
            return;
        }

        Queue<PendingCommand> queue = pendingCommands.get(key);
        if (queue == null || queue.isEmpty() || storageObject.getState() == StorageObjectState.CREATE) {
            return;
        }

        while (!queue.isEmpty()) {
            Command command = queue.peek().command;
            Optional<Throwable> error = new ValidatorChain<Throwable>()
                    .validate(() -> checkLockTokenIsValid(storageObject, command.getLockToken()))
                    .validate(() -> checkVerticleCanCoordinateCommand(command))
                    .getError();
            if (error.isPresent()) {
                // Reject the command
                queue.remove();
                command.getPromise().fail(error.get());
                continue;
            }
            // Check if we can handle the command now
            if ((!storageObject.isLocked()
                    // If a lock token is provided, it is guaranteed to be correct due to the check above
                    || command.getLockToken() != null)
                    && ((!command.isReadOnly() || storageObject.getState() == StorageObjectState.VALID)
                    || (command.isReadOnly() && command.isAllowInvalidReadsEnabled()))) {
                queue.remove();
                coordinateCommand(command);
            } else {
                // Wait until we can handle the command
                return;
            }
        }
    }

    private void coordinateCommand(Command command) {
        StorageObject storageObject = objects.get(command.getKey());

        if (!command.isReadOnly()) {
            // Set the state to invalid and increment the timestamp
            storageObject.setState(StorageObjectState.INVALID);
            storageObject.getTimestamp().setVersion(storageObject.getTimestamp().getVersion() + 1);
            storageObject.getTimestamp().setCoordinatorVerticleId(verticleId);
        }

        // Apply the command locally
        boolean succeeded = false;
        Object result;
        try {
            result = command.apply(this);
            succeeded = true;
        } catch (Exception e) {
            logger.debug("Error while applying command", e);
            result = e;
            // Continue replication as the command may have changed the state. We assume that
            // all replicas will get the same error.
        }

        if (command.isReadOnly() || ((InvalidationCommand) command).isAsyncReplicationEnabled()) {
            if (succeeded) {
                command.getPromise().complete(result);
            } else {
                command.getPromise().fail((Throwable) result);
            }
            if (command.isReadOnly()) {
                // Replication of read-only commands is not required
                return;
            }
        }

        // Create a copy of the timestamp as the timestamp in storageObject might change during replication
        Timestamp commandTimestamp = new Timestamp(storageObject.getTimestamp());

        // Replicate the command
        final boolean finalSucceeded = succeeded; // Required to be used in the lambda below
        final Object finalResult = result;
        invalidateReplicas((InvalidationCommand) command, commandTimestamp)
                .compose(res -> {
                    // Validate the object locally if there is no write operation with a higher timestamp
                    if (commandTimestamp.equals(storageObject.getTimestamp())) {
                        storageObject.setState(StorageObjectState.VALID);
                        handlePendingCommandsAsync(command.getKey());
                    }
                    if (!((InvalidationCommand) command).isAsyncReplicationEnabled()) {
                        // All replicas acknowledged the command, so we can complete the promise
                        if (finalSucceeded) {
                            command.getPromise().complete(finalResult);
                        } else {
                            command.getPromise().fail((Throwable) finalResult);
                        }
                    }
                    return Future.succeededFuture();
                })
                .compose(res -> commitReplicas(command.getKey(), commandTimestamp))
                .onFailure(err ->
                    // In case the client promise has not been completed yet, complete it with the error
                    command.getPromise().tryFail(err)
                );
    }

    private Future<Void> invalidateReplicas(InvalidationCommand command, Timestamp writeTimestamp) {
        Promise<Void> replicaInvalidationPromise = Promise.promise();
        invalidateReplicasWithRetries(command, writeTimestamp, replicaInvalidationPromise);
        return replicaInvalidationPromise.future();
    }

    @SuppressWarnings("rawtypes")
    private void invalidateReplicasWithRetries(InvalidationCommand command, Timestamp writeTimestamp, Promise<Void> promise) {
        StorageObject storageObject = objects.get(command.getKey());
        Optional<Throwable> error = new ValidatorChain<Throwable>()
                .validate(() -> checkObjectExists(storageObject))
                .validate(() -> checkVerticleIsPrimaryReplicaForKey(command.getKey()))
                .getError();
        if (error.isPresent()) {
            promise.fail(error.get());
            return;
        }

        KeyMetadata metadata = metadataService.getMetadataEntry(command.getKey()).getMetadata();
        Set<Integer> replicas = new HashSet<>(metadata.getObjectLocations());
        replicas.remove(verticleId);
        List<Future> rpcFutures = new ArrayList<>();
        for (int replicaVerticleId : replicas) {
            rpcFutures.add(storageRpcService.invalidate(replicaVerticleId, writeTimestamp, command));
        }
        CompositeFuture compositeFuture = CompositeFuture.join(rpcFutures);
        compositeFuture
                .onSuccess(res -> promise.complete())
                .onFailure(err -> {
                    logger.debug("Failed to invalidate replicas of object with key " + command.getKey(), err);
                    // Check the cause of the failure
                    for (Throwable cause : compositeFuture.causes()) {
                        if (cause instanceof StorageRpcException && !(command instanceof StateReplicationCommand)) {
                            StorageRpcException rpcException = (StorageRpcException) cause;
                            if (rpcException.getErrorType() == StorageRpcErrorType.MISSING_MESSAGES
                                    || rpcException.getErrorType() == StorageRpcErrorType.CONFLICTING_TIMESTAMPS) {
                                // At least one replica cannot apply the command due to missing messages or a
                                // diverged timestamp. We fix this by sending the whole state of the object.
                                InvalidationCommand stateReplicationCommand = new StateReplicationCommand(
                                        command.getPromise(), command.getKey(),
                                        command.getLockToken(), command.getOriginVerticleId(),
                                        storageObject);
                                vertx.setTimer(1000, timerId ->
                                        invalidateReplicasWithRetries(stateReplicationCommand, writeTimestamp, promise));
                                return;
                            }
                        }
                    }
                    // Wait a bit and retry
                    vertx.setTimer(1000, timerId -> invalidateReplicasWithRetries(command, writeTimestamp, promise));
                });
    }

    private Future<Void> commitReplicas(String key, Timestamp writeTimestamp) {
        Promise<Void> replicaValidationPromise = Promise.promise();
        commitReplicasWithRetries(key, writeTimestamp, replicaValidationPromise);
        return replicaValidationPromise.future();
    }

    @SuppressWarnings("rawtypes")
    private void commitReplicasWithRetries(String key, Timestamp writeTimestamp, Promise<Void> promise) {
        StorageObject storageObject = objects.get(key);
        Optional<Throwable> error = new ValidatorChain<Throwable>()
                .validate(() -> checkObjectExists(storageObject))
                .validate(() -> checkVerticleIsPrimaryReplicaForKey(key))
                .getError();
        if (error.isPresent()) {
            promise.fail(error.get());
            return;
        }

        // Check if there is a write operation with a higher timestamp
        if (writeTimestamp.getVersion() < storageObject.getTimestamp().getVersion()) {
            // Commit will be done by the new write
            promise.complete();
            return;
        }
        KeyMetadata metadata = metadataService.getMetadataEntry(key).getMetadata();
        Set<Integer> replicas = new HashSet<>(metadata.getObjectLocations());
        replicas.remove(verticleId);
        List<Future> rpcFutures = new ArrayList<>();
        for (int replicaVerticleId : replicas) {
            rpcFutures.add(storageRpcService.commit(replicaVerticleId, key, writeTimestamp));
        }
        CompositeFuture.join(rpcFutures)
                .onSuccess(res -> promise.complete())
                .onFailure(err -> {
                    logger.debug("Failed to validate replicas of object with key " + key, err);
                    // Wait a bit and retry
                    vertx.setTimer(1000, timerId -> commitReplicasWithRetries(key, writeTimestamp, promise));
                });
    }

    private void createObject(String key, Timestamp timestamp) {
        StorageObject storageObject = new StorageObject(timestamp);
        storageObject.setState(StorageObjectState.CREATE);
        objects.put(key, storageObject);
    }

    private void handlePendingCommandsAsync(String key) {
        Queue<PendingCommand> queue = pendingCommands.get(key);
        if (queue != null && !queue.isEmpty()) {
            vertx.runOnContext(v -> handlePendingCommands(key));
        }
    }

    private Future<Void> onMetadataServiceKeyInvalidated(String key, KeyMetadata oldMetadata, KeyMetadata newMetadata) {
        StorageObject storageObject = objects.get(key);
        if (storageObject == null && newMetadata.getObjectLocations().contains(verticleId)) {
            // Check whether the key is new or migrated
            if (oldMetadata == null) {
                createObject(key, new Timestamp(0, verticleId));
            } else {
                // Import the object from a verticle of the previous configuration
                return storageRpcService
                        .getObject(oldMetadata.getObjectLocations().iterator().next(), key)
                        .onSuccess(importedObject -> {
                            // Check if the key still exists
                            if (metadataService.getMetadataEntry(key) != null) {
                                objects.putIfAbsent(key, importedObject);
                            }
                        })
                        .onFailure(err -> logger.error("Failed to import object with key " + key, err))
                        .mapEmpty();

            }
        }
        return Future.succeededFuture();
    }

    private void onMetadataServiceKeyValidated(String key, KeyMetadata metadata) {
        // Check if the verticle is still responsible for this key
        if (metadata.getObjectLocations().contains(verticleId)) {
            StorageObject storageObject = objects.get(key);
            if (storageObject.getState() == StorageObjectState.CREATE) {
                storageObject.setState(StorageObjectState.VALID);
                handlePendingCommandsAsync(key);
            }
        } else {
            // Reject all pending commands for this key and remove the object
            Queue<PendingCommand> queue = pendingCommands.remove(key);
            if (queue != null) {
                queue.forEach(pending -> pending.command.getPromise().fail(new KeyDoesNotExistException()));
            }
            objects.remove(key);
        }
    }

    private KeyDoesNotExistException checkObjectExists(StorageObject storageObject) {
        return storageObject == null ? new KeyDoesNotExistException() : null;
    }

    private ObjectNotReadyException checkObjectIsReady(StorageObject storageObject) {
        return storageObject.getState() == StorageObjectState.CREATE ? new ObjectNotReadyException() : null;
    }

    private NotResponsibleException checkVerticleCanCoordinateCommand(Command command) {
        if (command.isReadOnly()) {
            return null;
        }
        return checkVerticleIsPrimaryReplicaForKey(command.getKey());
    }

    private NotResponsibleException checkVerticleIsPrimaryReplicaForKey(String key) {
        return getPrimaryReplica(key) == verticleId ? null : new NotResponsibleException();
    }

    private InvalidLockTokenException checkLockTokenIsValid(StorageObject storageObject, Integer lockToken) {
        if (lockToken == null) {
            return null;
        }
        if (!storageObject.isLocked()) {
            return new InvalidLockTokenException("Object is not locked");
        }
        if (!lockToken.equals(storageObject.getLockToken())) {
            return new InvalidLockTokenException("Lock token does not match");
        }
        return null;
    }

    private CommandRejectedException checkOriginIsPrimaryReplicaOfKey(String key, int originVerticleId) {
        return getPrimaryReplica(key) != originVerticleId ? new CommandRejectedException() : null;
    }

    private int getPrimaryReplica(String key) {
        KeyMetadata metadata = metadataService.getMetadataEntry(key).getMetadata();
        // The first element of the set is the primary replica
        return metadata.getObjectLocations().iterator().next();
    }

    protected enum CommandPriorityGroup {
        // Priorities need to be ordered from highest to lowest

        EXCLUSIVE_ACCESS_HIGH_PRIORITY,

        EXCLUSIVE_ACCESS_NORMAL_PRIORITY,

        HIGH,

        NORMAL
    }

    protected static class PendingCommand implements Comparable<PendingCommand> {

        protected final Command command;

        protected final int requestId;

        public PendingCommand(Command command, int requestId) {
            this.command = command;
            this.requestId = requestId;
        }

        @Override
        public int compareTo(PendingCommand other) {
            CommandPriorityGroup priorityGroup = getPriorityGroup(command);
            CommandPriorityGroup otherPriorityGroup = getPriorityGroup(other.command);

            if (priorityGroup.compareTo(otherPriorityGroup) < 0) {
                // This command has a higher priority than the other
                return -1;
            } else if (priorityGroup.compareTo(otherPriorityGroup) > 0) {
                // This command has a lower priority than the other
                return 1;
            } else {
                // Both commands are in the same priority group, we use the request ID as a tiebreaker (the command
                // with the lower request ID has a higher priority)
                return Integer.compare(requestId, other.requestId);
            }
        }

        @Override
        public boolean equals(Object o) {
            if (this == o) return true;
            if (o == null || getClass() != o.getClass()) return false;
            PendingCommand that = (PendingCommand) o;
            return requestId == that.requestId && command.equals(that.command);
        }

        @Override
        public int hashCode() {
            return Objects.hash(requestId, command);
        }

        protected CommandPriorityGroup getPriorityGroup(Command command) {
            if (command.getLockToken() != null) {
                return command.isAllowInvalidReadsEnabled()
                        ? CommandPriorityGroup.EXCLUSIVE_ACCESS_HIGH_PRIORITY
                        : CommandPriorityGroup.EXCLUSIVE_ACCESS_NORMAL_PRIORITY;
            }
            return command.isAllowInvalidReadsEnabled()
                    ? CommandPriorityGroup.HIGH
                    : CommandPriorityGroup.NORMAL;
        }
    }
}
