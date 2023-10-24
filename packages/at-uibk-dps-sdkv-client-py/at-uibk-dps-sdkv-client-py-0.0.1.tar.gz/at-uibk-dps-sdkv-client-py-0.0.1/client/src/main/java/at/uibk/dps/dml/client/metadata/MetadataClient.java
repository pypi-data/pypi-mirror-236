package at.uibk.dps.dml.client.metadata;

import at.uibk.dps.dml.client.BaseTcpClient;
import at.uibk.dps.dml.client.metadata.commands.*;
import io.vertx.core.Future;
import io.vertx.core.Vertx;

import java.util.Map;
import java.util.Set;

public class MetadataClient extends BaseTcpClient {

    public MetadataClient(Vertx vertx) {
        super(vertx);
    }

    public Future<Void> create(String key) {
        return create(key, null);
    }

    public Future<Void> create(String key, Set<Integer> replicaNodeIds) {
        if (replicaNodeIds != null && replicaNodeIds.isEmpty()) {
            throw new IllegalArgumentException();
        }
        return request(new CreateCommand(key, replicaNodeIds));
    }

    public Future<KeyConfiguration> get(String key) {
        return request(new GetCommand(key));
    }

    public Future<Map<String, KeyConfiguration>> getAll() {
        return request(new GetAllCommand());
    }

    public Future<Void> delete(String key) {
        return request(new DeleteCommand(key));
    }

    public Future<Void> reconfigure(String key, Set<Integer> newReplicaNodeIds) {
        if (newReplicaNodeIds == null || newReplicaNodeIds.isEmpty()) {
            throw new IllegalArgumentException();
        }
        return request(new ReconfigureCommand(key, newReplicaNodeIds));
    }

    @Override
    protected MetadataCommandError decodeCommandResultError(int errorCode, String message) {
        return new MetadataCommandError(MetadataCommandErrorType.valueOf(errorCode));
    }
}
