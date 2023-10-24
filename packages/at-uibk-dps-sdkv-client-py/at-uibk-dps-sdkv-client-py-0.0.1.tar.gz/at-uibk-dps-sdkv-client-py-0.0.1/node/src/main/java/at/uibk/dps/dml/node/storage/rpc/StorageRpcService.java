package at.uibk.dps.dml.node.storage.rpc;

import at.uibk.dps.dml.node.util.Timestamp;
import at.uibk.dps.dml.node.storage.StorageObject;
import at.uibk.dps.dml.node.storage.command.InvalidationCommand;
import io.vertx.core.Future;

public interface StorageRpcService {

    Future<Void> invalidate(int remoteVerticleId, Timestamp timestamp, InvalidationCommand command);

    Future<Void> commit(int remoteVerticleId, String key, Timestamp timestamp);

    Future<StorageObject> getObject(int remoteVerticleId, String key);

}
