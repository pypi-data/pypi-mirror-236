package at.uibk.dps.dml.client;

import at.uibk.dps.dml.client.metadata.*;
import at.uibk.dps.dml.client.storage.*;
import at.uibk.dps.dml.client.storage.object.Barrier;
import at.uibk.dps.dml.client.storage.object.SharedCounter;
import at.uibk.dps.dml.client.storage.object.SharedJson;
import io.vertx.core.CompositeFuture;
import io.vertx.core.Future;
import io.vertx.core.Promise;
import io.vertx.core.Vertx;

import java.util.*;
import java.util.function.Function;
import java.util.stream.Collectors;

public class DmlClient {

    private static final int MAX_RETRIES = 3;

    private static final String DEFAULT_OBJECT_TYPE = "SharedBuffer";

    private final Vertx vertx;

    private final StorageSelector storageSelector;

    private final SharedObjectArgsCodec sharedObjectArgsCodec;

    private final MetadataClient metadataClient;

    private final Map<Storage, StorageClient> storageConnections = new HashMap<>();

    private final Map<String, KeyConfiguration> keyConfigurationsCache = new HashMap<>();

    public DmlClient(Vertx vertx) {
        this(vertx, new SimpleStorageSelector(), new BsonArgsCodec());
    }

    public DmlClient(Vertx vertx, StorageSelector storageSelector, SharedObjectArgsCodec sharedObjectArgsCodec) {
        this.vertx = vertx;
        this.storageSelector = storageSelector;
        this.sharedObjectArgsCodec = sharedObjectArgsCodec;
        this.metadataClient = new MetadataClient(vertx);
    }

    public Future<Void> connect(String metadataServerHost, int metadataServerPort) {
        return metadataClient.connect(metadataServerHost, metadataServerPort);
    }

    @SuppressWarnings("rawtypes")
    public Future<Void> disconnect() {
        List<Future> futures = storageConnections.values().stream().map(BaseTcpClient::disconnect).collect(Collectors.toList());
        storageConnections.clear();
        futures.add(metadataClient.disconnect());
        Promise<Void> promise = Promise.promise();
        CompositeFuture.join(futures)
                .onSuccess(res -> promise.complete())
                .onFailure(promise::fail);
        return promise.future();
    }

    /**
     * Creates a {@value #DEFAULT_OBJECT_TYPE} accessible by the given key.
     * Does nothing if the key already exists.
     *
     * @param key the name of the object
     * @return a future that completes when the object has been created
     */
    public Future<Void> create(String key) {
        return create(key, null, DEFAULT_OBJECT_TYPE, null, true);
    }

    /**
     * Same as {@link #create(String)} but with additional arguments to be provided to the constructor of the
     * {@value #DEFAULT_OBJECT_TYPE}.
     *
     * @param key the name of the object
     * @param args the arguments
     * @return a future that completes when the object has been created
     */
    public Future<Void> create(String key, Object[] args) {
        return create(key, null, DEFAULT_OBJECT_TYPE, args, true);
    }

    /**
     * Same as {@link #create(String, Object[])} but allows to set the node IDs storing replicas of the object.
     *
     * @param key the name of the object
     * @param replicaNodeIds the node IDs of the replicas
     * @param args the arguments
     * @return a future that completes when the object has been created
     */
    public Future<Void> create(String key, Set<Integer> replicaNodeIds, Object[] args) {
        return create(key, replicaNodeIds, DEFAULT_OBJECT_TYPE, args, true);
    }

    /**
     * Creates a shared object of the given type accessible by the given key.
     * Does nothing if the key already exists.
     *
     * @param key the name of the object
     * @return a future that completes when the object has been created
     */
    public Future<Void> create(String key, String objectType) {
        return create(key, null, objectType, null, true);
    }

    /**
     * Same as {@link #create(String, String)} but with additional arguments to be provided to the constructor of the
     * object.
     *
     * @param key the name of the object
     * @param args the arguments
     * @return a future that completes when the object has been created
     */
    public Future<Void> create(String key, String objectType, Object[] args) {
        return create(key, null, objectType, args, true);
    }

    /**
     * Creates a shared object.
     *
     * @param key the name of the object
     * @param replicaNodeIds the node IDs storing replicas or {@code null} if the replicas should be selected
     *                       automatically
     * @param objectType the type of the object
     * @param args the arguments to be provided to the constructor of the object
     * @param ignoreIfAlreadyExists if {@code true}, the method does nothing if the key already exists;
     *                              if {@code false}, it fails if the key already exists
     * @return a future that completes when the object has been created
     */
    public Future<Void> create(String key, Set<Integer> replicaNodeIds, String objectType, Object[] args,
                               boolean ignoreIfAlreadyExists) {
        if (replicaNodeIds != null && replicaNodeIds.isEmpty()) {
            throw new IllegalArgumentException();
        }
        return metadataClient
                .create(key, replicaNodeIds)
                .compose(res ->
                        executeStorageCommandForExistingKey(key,
                                storageClient -> storageClient.initObject(key, "java", objectType, args, null)
                        )
                )
                .recover(err -> {
                    if (ignoreIfAlreadyExists && err instanceof MetadataCommandError) {
                        MetadataCommandError error = (MetadataCommandError) err;
                        if (error.getErrorType() == MetadataCommandErrorType.KEY_ALREADY_EXISTS) {
                            return Future.succeededFuture();
                        }
                    }
                    return Future.failedFuture(err);
                });
    }

    /**
     * Creates a {@link SharedCounter}.
     *
     * @param key the name of the shared counter
     * @return a future that completes when the shared counter has been created
     */
    public Future<SharedCounter> createSharedCounter(String key) {
        return create(key, "SharedCounter").map(res -> new SharedCounter(this, key));
    }

    /**
     * Creates an empty {@link SharedJson} document.
     *
     * @param key the name of the shared JSON document
     * @return a future that completes when the shared JSON document has been created
     */
    public Future<SharedJson> createSharedJson(String key) {
        return create(key, "SharedJson").map(res -> new SharedJson(this, key));
    }

    /**
     * Creates a {@link SharedJson} document with the given content.
     *
     * @param key the name of the shared JSON document
     * @param content the initial content of the document
     * @return a future that completes when the shared JSON document has been created
     */
    public Future<SharedJson> createSharedJson(String key, Object content) {
        return create(key, "SharedJson", new Object[]{content}).map(res -> new SharedJson(this, key));
    }

    /**
     * Creates a {@link Barrier}.
     *
     * @param key the name of the barrier
     * @param parties the number of parties that must wait on the barrier
     * @return a future that completes when the barrier has been created
     */
    public Future<Barrier> createBarrier(String key, int parties) {
        return createSharedCounter(key).map(res -> new Barrier(vertx, parties, res));
    }

    /**
     * Same as {@link #createBarrier(String, int)} but allows to configure the delay to wait between checks of the
     * barrier state.
     *
     * @param key the name of the barrier
     * @param parties the number of parties that must wait on the barrier
     * @param checkDelayMs the delay to wait between checks of the barrier state
     * @return a future that completes when the barrier has been created
     */
    public Future<Barrier> createBarrier(String key, int parties, int checkDelayMs) {
        return createSharedCounter(key).map(res -> new Barrier(vertx, parties, res, checkDelayMs));
    }

    /**
     * Returns the value of the object with the given key. Assumes that the object is a {@value #DEFAULT_OBJECT_TYPE}.
     *
     * @param key the name of the object
     * @return a future that completed with the value of the object
     */
    public Future<byte[]> get(String key) {
        return get(key, null, false);
    }

    /**
     * Same as {@link #get(String)} but with a lock token.
     *
     * @param key the name of the object
     * @param lockToken the lock token or {@code null} if no lock token should be used
     * @return a future that completed with the value of the object
     */
    public Future<byte[]> get(String key, Integer lockToken) {
        return get(key, lockToken, false);
    }

    /**
     * Same as {@link #get(String, Integer)} but allows to read invalid (uncommitted) values.
     *
     * @param key the name of the object
     * @param lockToken the lock token or {@code null} if no lock token should be used
     * @param allowInvalidReads if {@code true}, the method may return an invalid (uncommitted) value
     * @return a future that completed with the value of the object
     */
    public Future<byte[]> get(String key, Integer lockToken, boolean allowInvalidReads) {
        Set<Flag> flags = allowInvalidReads
                ? EnumSet.of(Flag.READ_ONLY, Flag.ALLOW_INVALID_READS)
                : EnumSet.of(Flag.READ_ONLY);
        return invokeMethod(key, "get", null, lockToken, flags).map(byte[].class::cast);
    }

    /**
     * Sets the value of the object with the given key. Assumes that the object is a {@value #DEFAULT_OBJECT_TYPE}.
     *
     * @param key the name of the object
     * @param value the new value of the object
     * @return a future that completes when the value has been set
     */
    public Future<Void> set(String key, byte[] value) {
        return set(key, value, null, false);
    }

    /**
     * Same as {@link #set(String, byte[])} but with a lock token.
     *
     * @param key the name of the object
     * @param value the new value of the object
     * @param lockToken the lock token or {@code null} if no lock token should be used
     * @return a future that completes when the value has been set
     */
    public Future<Void> set(String key, byte[] value, Integer lockToken) {
        return set(key, value, lockToken, false);
    }

    /**
     * Same as {@link #set(String, byte[], Integer)} but allows to configure asynchronous replication.
     *
     * @param key the name of the object
     * @param value the new value of the object
     * @param asyncReplication if {@code true}, the future may complete before the value has been fully replicated
     * @return a future that completes when the value has been set
     */
    public Future<Void> set(String key, byte[] value, boolean asyncReplication) {
        return set(key, value, null, asyncReplication);
    }

    /**
     * Same as {@link #set(String, byte[], boolean)} but with a lock token.
     *
     * @param key the name of the object
     * @param value the new value of the object
     * @param lockToken the lock token or {@code null} if no lock token should be used
     * @param asyncReplication if {@code true}, the future may complete before the value has been fully replicated
     * @return a future that completes when the value has been set
     */
    public Future<Void> set(String key, byte[] value, Integer lockToken, boolean asyncReplication) {
        Set<Flag> flags = asyncReplication ? EnumSet.of(Flag.ASYNC_REPLICATION) : EnumSet.noneOf(Flag.class);
        return invokeMethod(key, "set", new Object[]{value}, lockToken, flags).mapEmpty();
    }

    /**
     * Invokes a method on the object with the given key.
     * 
     * @param key the name of the object
     * @param methodName the name of the method to invoke
     * @param args the arguments to be provided to the method
     * @return a future that completed with the result of the method invocation
     */
    public Future<Object> invokeMethod(String key, String methodName, Object[] args) {
        return invokeMethod(key, methodName, args, null, EnumSet.noneOf(Flag.class));
    }

    /**
     * Same as {@link #invokeMethod(String, String, Object[])} but with a lock token.
     * 
     * @param key the name of the object
     * @param methodName the name of the method to invoke
     * @param args the arguments to be provided to the method
     * @param lockToken the lock token or {@code null} if no lock token should be used
     * @return a future that completed with the result of the method invocation
     */
    public Future<Object> invokeMethod(String key, String methodName, Object[] args, Integer lockToken) {
        return invokeMethod(key, methodName, args, lockToken, EnumSet.noneOf(Flag.class));
    }

    /**
     * Same as {@link #invokeMethod(String, String, Object[])} but allows to add additional flags.
     * 
     * @param key the name of the object
     * @param methodName the name of the method to invoke
     * @param args the arguments to be provided to the method
     * @param flags the flags to be used
     * @return a future that completed with the result of the method invocation
     */
    public Future<Object> invokeMethod(String key, String methodName, Object[] args, Set<Flag> flags) {
        return invokeMethod(key, methodName, args, null, flags);
    }

    /**
     * Same as {@link #invokeMethod(String, String, Object[], Integer)} but allows to add additional flags.
     * 
     * @param key the name of the object
     * @param methodName the name of the method to invoke
     * @param args the arguments to be provided to the method
     * @param lockToken the lock token or {@code null} if no lock token should be used
     * @param flags the flags to be used
     * @return a future that completed with the result of the method invocation
     */
    public Future<Object> invokeMethod(String key, String methodName, Object[] args, Integer lockToken,
                                       Set<Flag> flags) {
        return executeStorageCommandForExistingKey(key, storageClient ->
                storageClient.invokeMethod(key, methodName, args, lockToken, flags));
    }

    /**
     * Locks the object with the given key. Returns a lock token that must be used for all subsequent operations on
     * the object and to unlock it. Requests without the lock token will be queued or rejected.
     *
     * @param key the name of the object
     * @return a future that completes with the lock token
     */
    public Future<Integer> lock(String key) {
        return executeStorageCommandForExistingKey(key, storageClient -> storageClient.lock(key));
    }

    /**
     * Unlocks the object with the given key using the given lock token.
     *
     * @param key the name of the object
     * @param lockToken the lock token returned by the lock method
     * @return a future that completed when the object has been unlocked
     */
    public Future<Void> unlock(String key, int lockToken) {
        return executeStorageCommandForExistingKey(key, storageClient -> storageClient.unlock(key, lockToken));
    }

    /**
     * Deletes the object with the given key.
     *
     * @param key the name of the object
     * @return a future that completed when the object has been deleted
     */
    public Future<Void> delete(String key) {
        return metadataClient.delete(key).onSuccess(res -> keyConfigurationsCache.remove(key));
    }

    /**
     * Migrates the object with the given key to the specified replicas.
     *
     * @param key the name of the object
     * @param newReplicaNodeIds the node IDs of the new replicas
     * @return a future that completed when the object has been migrated
     */
    public Future<Void> reconfigure(String key, Set<Integer> newReplicaNodeIds) {
        if (newReplicaNodeIds == null || newReplicaNodeIds.isEmpty()) {
            throw new IllegalArgumentException();
        }
        return metadataClient.reconfigure(key, newReplicaNodeIds).onSuccess(res -> keyConfigurationsCache.remove(key));
    }

    /**
     * Returns the configuration of all keys.
     *
     * @return a future that completes with a map from keys to their configurations
     */
    public Future<Map<String, KeyConfiguration>> getAllConfigurations() {
        return getAllConfigurations(false);
    }

    /**
     * Returns the configuration of all keys.
     *
     * @param fillCache if {@code true}, the client's configuration cache is filled with the result
     * @return a future that completes with a map from keys to their configurations
     */
    public Future<Map<String, KeyConfiguration>> getAllConfigurations(boolean fillCache) {
        return metadataClient.getAll().onSuccess(configs -> {
            if (fillCache) {
                keyConfigurationsCache.putAll(configs);
            }
        });
    }

    private Future<StorageClient> getOrCreateStorageClient(Storage storage) {
        StorageClient cachedClient = storageConnections.get(storage);
        if (cachedClient != null) {
            return Future.succeededFuture(cachedClient);
        }
        Promise<StorageClient> promise = Promise.promise();
        StorageClient storageClient = new StorageClient(vertx, sharedObjectArgsCodec);
        storageClient.connect(storage.getHostname(), storage.getPort())
                .onSuccess(res -> {
                    storageConnections.put(storage, storageClient);
                    storageClient.disconnectHandler(v -> storageConnections.remove(storage, storageClient));
                    promise.complete(storageClient);
                })
                .onFailure(promise::fail);
        return promise.future();
    }

    private <T> Future<T> executeStorageCommandForExistingKey(
            String key, Function<StorageClient, Future<Response<T>>> command) {
        Promise<T> promise = Promise.promise();
        executeStorageCommandForExistingKeyWithRetries(key, command, 1, MAX_RETRIES, promise);
        return promise.future();
    }

    private <T> void executeStorageCommandForExistingKeyWithRetries(
            String key, Function<StorageClient, Future<Response<T>>> command,
            int attempt, int maxAttempts, Promise<T> promise) {
        KeyConfiguration cachedConfiguration = keyConfigurationsCache.get(key);
        Future<KeyConfiguration> future = cachedConfiguration != null
                ? Future.succeededFuture(cachedConfiguration)
                : Future.failedFuture("");

        future
                // Key configuration not in the cache -> get it from the metadata server
                .recover(err -> metadataClient.get(key).onSuccess(keyConfig -> keyConfigurationsCache.put(key, keyConfig)))
                .compose(keyConfig -> {
                    // Select a storage node and connect to it
                    Storage storage = storageSelector.select(keyConfig.getReplicas());
                    return getOrCreateStorageClient(storage);
                })
                // Execute the command
                .compose(command)
                .onSuccess(response -> {
                    promise.complete(response.getResult());
                    KeyConfiguration keyConfig = keyConfigurationsCache.get(key);
                    if (keyConfig != null && keyConfig.getVersion() != response.getMetadataVersion()) {
                        // Key configuration is outdated, remove it from the cache (the result is still valid)
                        keyConfigurationsCache.remove(key);
                    }
                })
                .onFailure(err -> {
                    if (err instanceof StorageCommandError) {
                        StorageCommandErrorType errorType = ((StorageCommandError) err).getErrorType();
                        if (errorType == StorageCommandErrorType.KEY_DOES_NOT_EXIST
                                || errorType == StorageCommandErrorType.NOT_RESPONSIBLE) {
                            // Key might have been migrated to other storage nodes, remove the configuration
                            // from the cache and retry
                            keyConfigurationsCache.remove(key);
                            if (attempt < maxAttempts) {
                                executeStorageCommandForExistingKeyWithRetries(
                                        key, command, attempt + 1, maxAttempts, promise
                                );
                                return;
                            }
                        }
                        if (errorType == StorageCommandErrorType.OBJECT_NOT_INITIALIZED && attempt < maxAttempts) {
                            // Another client might have just created the object but not yet initialized it, wait a
                            // bit and retry
                            vertx.setTimer(25, timerId -> executeStorageCommandForExistingKeyWithRetries(
                                    key, command, attempt + 1, maxAttempts, promise)
                            );
                            return;
                        }
                    }
                    promise.fail(err);
                });
    }
}
