package at.uibk.dps.dml.node.metadata;

import at.uibk.dps.dml.client.metadata.KeyConfiguration;
import at.uibk.dps.dml.client.metadata.Storage;
import at.uibk.dps.dml.node.exception.*;
import at.uibk.dps.dml.node.util.Timestamp;
import at.uibk.dps.dml.node.membership.MembershipManager;
import at.uibk.dps.dml.node.membership.MembershipView;
import at.uibk.dps.dml.node.membership.VerticleInfo;
import at.uibk.dps.dml.node.membership.VerticleType;
import at.uibk.dps.dml.node.metadata.command.*;
import at.uibk.dps.dml.node.metadata.rpc.*;
import at.uibk.dps.dml.node.util.ValidatorChain;
import io.vertx.core.*;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.*;
import java.util.stream.Collectors;

public class MetadataService implements CommandHandler {

    private final Logger logger = LoggerFactory.getLogger(MetadataService.class);

    private final Vertx vertx;

    private final VerticleInfo verticleInfo;

    private final MetadataRpcService metadataRpcService;

    private final StorageMapper storageMapper;
    /**
     * Maps keys to pending commands
     */
    private final Map<String, Queue<PendingCommand>> pendingCommands = new HashMap<>();

    private final Map<String, MetadataEntry> keyMetadataMap = new HashMap<>();

    private MembershipView membershipView;

    /**
     * Contains the verticle IDs of all metadata verticles in the current membership view.
     */
    private Set<Integer> metadataVerticleIds;

    private MetadataChangeListener listener;

    private int requestCounter = 0;

    public MetadataService(Vertx vertx, MembershipManager membershipManager,
                           VerticleInfo verticleInfo, MetadataRpcService metadataRpcService,
                           StorageMapper storageMapper) {
        this.vertx = vertx;
        this.verticleInfo = verticleInfo;
        this.metadataRpcService = metadataRpcService;
        this.storageMapper = storageMapper;
        membershipManager.addListener(view -> vertx.runOnContext(event -> onMembershipChange(view)));
        onMembershipChange(membershipManager.getMembershipView());
    }

    @SuppressWarnings({"rawtypes", "unchecked"})
    public Future<Void> create(String key, Set<Integer> objectLocations) {
        if (keyMetadataMap.containsKey(key)) {
            return Future.failedFuture(new KeyAlreadyExistsException());
        }

        if (objectLocations == null || objectLocations.isEmpty()) {
            objectLocations = storageMapper.select(
                    membershipView.getNodeMap().values(),
                    verticleInfo.getOwnerNode().getDefaultNumReplicas());
        } else if (!membershipView.getVerticleIdsByType(VerticleType.STORAGE).containsAll(objectLocations)) {
            return Future.failedFuture(new InvalidObjectLocationsException());
        }

        createMetadataEntry(key, new Timestamp(0, verticleInfo.getId()));

        Promise promise = Promise.promise();
        enqueueCommand(new CreateCommand(promise, key, new KeyMetadata(objectLocations)));
        return promise.future();
    }

    @SuppressWarnings({"rawtypes", "unchecked"})
    public Future<KeyConfiguration> get(String key) {
        MetadataEntry metadataEntry = keyMetadataMap.get(key);
        if (metadataEntry == null) {
            return Future.failedFuture(new KeyDoesNotExistException());
        }
        Promise promise = Promise.promise();
        enqueueCommand(new GetCommand(promise, key));
        return promise.future();
    }

    @SuppressWarnings({"rawtypes", "unchecked"})
    public Future<Map<String, KeyConfiguration>> getAll() {
        Promise promise = Promise.promise();
        enqueueCommand(new GetAllCommand(promise));
        return promise.future();
    }

    @SuppressWarnings({"rawtypes", "unchecked"})
    public Future<Void> reconfigure(String key, Set<Integer> objectLocations) {
        if (!membershipView.getVerticleIdsByType(VerticleType.STORAGE).containsAll(objectLocations)) {
            return Future.failedFuture(new InvalidObjectLocationsException());
        }
        Promise promise = Promise.promise();
        enqueueCommand(new ReconfigureCommand(promise, key, new KeyMetadata(objectLocations)));
        return promise.future();
    }

    @SuppressWarnings({"rawtypes", "unchecked"})
    public Future<Void> delete(String key) {
        Promise promise = Promise.promise();
        enqueueCommand(new DeleteCommand(promise, key));
        return promise.future();
    }

    public MetadataEntry getMetadataEntry(String key) {
        return keyMetadataMap.get(key);
    }

    public Future<Void> invalidate(Timestamp timestamp, InvalidationCommand command) {
        MetadataEntry metadataEntry = keyMetadataMap.get(command.getKey());
        if (metadataEntry == null
                && (command.getType() == InvalidationCommandType.CREATE
                || command.getType() == InvalidationCommandType.RECONFIGURE)) {
            metadataEntry = createMetadataEntry(command.getKey(), new Timestamp(0, verticleInfo.getId()));
        } else if (metadataEntry == null) {
            return Future.failedFuture(new KeyDoesNotExistException());
        }

        Timestamp localTimestamp = metadataEntry.getTimestamp();
        if (!timestamp.isGreaterThan(localTimestamp)) {
            // We already received a command with a higher timestamp, we simply ACK it
            return Future.succeededFuture();
        }

        metadataEntry.setState(MetadataEntryState.INVALID);
        localTimestamp.setVersion(timestamp.getVersion());
        localTimestamp.setCoordinatorVerticleId(timestamp.getCoordinatorVerticleId());
        metadataEntry.setOldMetadata(command.getOldMetadata());

        try {
            command.apply(this);
        } catch (Exception e) {
            return Future.failedFuture(e);
        }

        if (timestamp.equals(localTimestamp) && listener != null) {
            return listener.keyInvalidated(command.getKey(), metadataEntry.getOldMetadata(), metadataEntry.getMetadata());
        }

        return Future.succeededFuture();
    }

    public Future<Void> commit(String key, Timestamp timestamp) {
        MetadataEntry metadataEntry = keyMetadataMap.get(key);
        if (metadataEntry == null) {
            return Future.failedFuture(new KeyDoesNotExistException());
        }

        commitIfTimestampIsMostRecent(key, metadataEntry, timestamp);

        return Future.succeededFuture();
    }

    public void setListener(MetadataChangeListener listener) {
        this.listener = listener;
    }

    @Override
    public Object apply(CreateCommand command) {
        MetadataEntry metadataEntry = keyMetadataMap.get(command.getKey());
        metadataEntry.setMetadata(command.getMetadata());
        return null;
    }

    @Override
    public Object apply(GetCommand command) {
        MetadataEntry metadataEntry = keyMetadataMap.get(command.getKey());
        return getConfigurationForKey(metadataEntry);
    }

    @Override
    public Object apply(GetAllCommand command) {
        Map<String, KeyConfiguration> result = new HashMap<>();
        for (Map.Entry<String, MetadataEntry> entry : keyMetadataMap.entrySet()) {
            result.put(entry.getKey(), getConfigurationForKey(entry.getValue()));
        }
        return result;
    }

    @Override
    public Object apply(ReconfigureCommand command) {
        MetadataEntry metadataEntry = keyMetadataMap.get(command.getKey());
        metadataEntry.setMetadata(command.getNewMetadata());
        return null;
    }

    @Override
    public Object apply(DeleteCommand command) {
        MetadataEntry metadataEntry = keyMetadataMap.get(command.getKey());
        metadataEntry.setMetadata(new KeyMetadata(Collections.emptySet()));
        return null;
    }

    private MetadataEntry createMetadataEntry(String key, Timestamp timestamp) {
        MetadataEntry metadataEntry = new MetadataEntry(timestamp);
        metadataEntry.setState(MetadataEntryState.INVALID);
        keyMetadataMap.put(key, metadataEntry);
        return metadataEntry;
    }

    private void enqueueCommand(Command command) {
        if (command.getKey() == null && command.isReadOnly() && command.isAllowInvalidReadsEnabled()) {
            // No need to queue this command, we can execute it immediately
            coordinateCommand(command);
            return;
        } else if (command.getKey() == null) {
            command.getPromise().fail(new IllegalArgumentException("Key must not be null"));
            return;
        }

        MetadataEntry metadataEntry = keyMetadataMap.get(command.getKey());
        Optional<Throwable> error = new ValidatorChain<Throwable>()
                .validate(() -> checkKeyExists(metadataEntry))
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
        MetadataEntry metadataEntry = keyMetadataMap.get(key);
        if (metadataEntry == null) {
            return;
        }

        Queue<PendingCommand> queue = pendingCommands.get(key);
        if (queue == null || queue.isEmpty()) {
            return;
        }

        while (!queue.isEmpty()) {
            Command command = queue.peek().command;
            // Check if we can handle the command straight away
            if ((!command.isReadOnly() || metadataEntry.getState() == MetadataEntryState.VALID || command instanceof CreateCommand)
                    || (command.isReadOnly() && command.isAllowInvalidReadsEnabled())) {
                queue.remove();
                coordinateCommand(command);
            } else {
                // Wait until we can handle the command
                return;
            }
        }
    }

    private void coordinateCommand(Command command) {
        MetadataEntry metadataEntry = keyMetadataMap.get(command.getKey());

        if (!command.isReadOnly()) {
            metadataEntry.setState(MetadataEntryState.INVALID);

            Timestamp timestamp = metadataEntry.getTimestamp();
            if (command instanceof DeleteCommand) {
                // We increment the version by 2 so a delete operation racing with another command always has a higher
                // timestamp
                timestamp.setVersion(timestamp.getVersion() + 2);
            } else {
                timestamp.setVersion(timestamp.getVersion() + 1);
            }
            timestamp.setCoordinatorVerticleId(verticleInfo.getId());

            if (command instanceof InvalidationCommand) {
                metadataEntry.setOldMetadata(metadataEntry.getMetadata());
                ((InvalidationCommand) command).setOldMetadata(metadataEntry.getMetadata());
            }
        }

        // Apply the command locally
        Object result;
        try {
            result = command.apply(this);
        } catch (Exception e) {
            command.getPromise().fail(e);
            return;
        }

        if (command.isReadOnly()) {
            command.getPromise().complete(result);
            // Replication of read-only commands is not required
            return;
        }

        // Create a copy of the timestamp as the timestamp in the metadata entry might change during replication
        Timestamp commandTimestamp = new Timestamp(metadataEntry.getTimestamp());

        // Replicate the command
        invalidateReplicas((InvalidationCommand) command, commandTimestamp)
                .compose(res -> {
                    // All metadata replicas acknowledged the invalidation, so we can complete the request promise
                    command.getPromise().complete(result);
                    return commitReplicas(command.getKey(), commandTimestamp);
                })
                .onSuccess(res -> commitIfTimestampIsMostRecent(command.getKey(), metadataEntry, commandTimestamp))
                .onFailure(err ->
                        // In case the request promise has not been completed yet, complete it with the error
                        command.getPromise().tryFail(err)
                );
    }

    private Future<Void> invalidateReplicas(InvalidationCommand command, Timestamp writeTimestamp) {
        Promise<Void> replicaInvalidationPromise = Promise.promise();
        invalidateReplicasWithRetries(command, writeTimestamp, replicaInvalidationPromise);
        return replicaInvalidationPromise.future();
    }

    private void invalidateReplicasWithRetries(InvalidationCommand command, Timestamp writeTimestamp,
                                               Promise<Void> promise) {
        MetadataEntry metadataEntry = keyMetadataMap.get(command.getKey());
        Timestamp currentTimestamp = metadataEntry.getTimestamp();
        if (currentTimestamp.isGreaterThan(writeTimestamp)) {
            // We received a concurrent operation with a higher timestamp => abort
            promise.fail(new ConcurrentOperationException());
            return;
        }

        // First send the invalidation to all main metadata verticles and afterwards to the storage verticles of the
        // old and new configuration
        Set<Integer> destinations1 = new HashSet<>(metadataVerticleIds);
        destinations1.remove(verticleInfo.getId());
        sendInvalidations(destinations1, writeTimestamp, command)
                .compose(res -> {
                    Set<Integer> destinations2 = metadataEntry.getMetadata() != null
                            ? new HashSet<>(metadataEntry.getMetadata().getObjectLocations())
                            : new HashSet<>();
                    if (metadataEntry.getOldMetadata() != null) {
                        destinations2.addAll(metadataEntry.getOldMetadata().getObjectLocations());
                    }
                    destinations2.remove(verticleInfo.getId());
                    return sendInvalidations(destinations2, writeTimestamp, command);
                })
                .onSuccess(res -> promise.complete())
                .onFailure(err -> {
                    logger.debug("Failed to invalidate metadata replicas of key " + command.getKey(), err);
                    // Wait a bit and retry
                    vertx.setTimer(1000, timerId -> invalidateReplicasWithRetries(command, writeTimestamp, promise));
                });
    }

    @SuppressWarnings("rawtypes")
    private CompositeFuture sendInvalidations(Set<Integer> destinations, Timestamp writeTimestamp,
                                              InvalidationCommand command) {
        List<Future> rpcFutures = new ArrayList<>();
        for (int verticleId : destinations) {
            rpcFutures.add(metadataRpcService.invalidate(verticleId, writeTimestamp, command));
        }
        return CompositeFuture.join(rpcFutures);
    }

    private void commitIfTimestampIsMostRecent(String key, MetadataEntry metadataEntry, Timestamp timestamp) {
        if (!timestamp.equals(metadataEntry.getTimestamp())) {
            return;
        }

        metadataEntry.setOldMetadata(null);
        metadataEntry.setState(MetadataEntryState.VALID);
        if (listener != null) {
            listener.keyValidated(key, metadataEntry.getMetadata());
        }

        // Check if we are still responsible for this key
        if (metadataEntry.getMetadata().getObjectLocations().isEmpty()
                || (verticleInfo.getType() == VerticleType.STORAGE
                && !metadataEntry.getMetadata().getObjectLocations().contains(verticleInfo.getId()))) {
            // Reject all pending commands and delete the key
            Queue<PendingCommand> queue = pendingCommands.remove(key);
            if (queue != null) {
                queue.forEach(pending -> pending.command.getPromise().fail(new KeyDoesNotExistException()));
            }
            keyMetadataMap.remove(key);
        } else {
            vertx.runOnContext(v -> handlePendingCommands(key));
        }
    }

    private Future<Void> commitReplicas(String key, Timestamp writeTimestamp) {
        Promise<Void> replicaValidationPromise = Promise.promise();
        commitReplicasWithRetries(key, writeTimestamp, replicaValidationPromise);
        return replicaValidationPromise.future();
    }

    private void commitReplicasWithRetries(String key, Timestamp writeTimestamp, Promise<Void> promise) {
        MetadataEntry metadataEntry = keyMetadataMap.get(key);
        Set<Integer> metadataLocations = getMetadataReplicaLocations(metadataEntry);

        @SuppressWarnings("rawtypes")
        List<Future> rpcFutures = new ArrayList<>();
        for (Integer location : metadataLocations) {
            rpcFutures.add(metadataRpcService.commit(location, key, writeTimestamp));
        }
        CompositeFuture.join(rpcFutures)
                .onSuccess(res -> promise.complete())
                .onFailure(err -> {
                    logger.debug("Failed to validate metadata replicas of object with key " + key, err);
                    // Wait a bit and retry
                    vertx.setTimer(1000, timerId -> commitReplicasWithRetries(key, writeTimestamp, promise));
                });
    }

    private Set<Integer> getMetadataReplicaLocations(MetadataEntry metadataEntry) {
        Set<Integer> locations = new HashSet<>(metadataVerticleIds);
        locations.addAll(metadataEntry.getMetadata().getObjectLocations());
        if (metadataEntry.getOldMetadata() != null) {
            locations.addAll(metadataEntry.getOldMetadata().getObjectLocations());
        }
        locations.remove(verticleInfo.getId());
        return locations;
    }

    private KeyConfiguration getConfigurationForKey(MetadataEntry metadataEntry) {
        if (metadataEntry.getMetadata() == null) {
            return null;
        }
        List<Storage> storages = metadataEntry.getMetadata().getObjectLocations().stream()
                .map(verticleId -> {
                    VerticleInfo verticle = membershipView.findVerticleById(verticleId);
                    return new Storage(
                            verticle.getId(),
                            verticle.getOwnerNode().getRegion(),
                            verticle.getOwnerNode().getHostname(),
                            verticle.getPort()
                    );
                })
                .collect(Collectors.toList());
        return new KeyConfiguration((int) metadataEntry.getTimestamp().getVersion(), storages);
    }

    private void onMembershipChange(MembershipView membershipView) {
        if (membershipView == null ||
                (this.membershipView != null && membershipView.getEpoch() <= this.membershipView.getEpoch())) {
            return;
        }
        this.membershipView = membershipView;
        metadataVerticleIds = membershipView.getNodeMap().values().stream()
                .flatMap(node -> node.getVerticles().stream())
                .filter(verticle -> verticle.getType() == VerticleType.METADATA)
                .map(VerticleInfo::getId)
                .collect(Collectors.toSet());
    }

    private KeyDoesNotExistException checkKeyExists(MetadataEntry metadataEntry) {
        return metadataEntry == null ? new KeyDoesNotExistException() : null;
    }

    protected enum CommandPriorityGroup {
        // Priorities need to be ordered from highest to lowest

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
            return command.isAllowInvalidReadsEnabled()
                    ? CommandPriorityGroup.HIGH
                    : CommandPriorityGroup.NORMAL;
        }
    }
}
