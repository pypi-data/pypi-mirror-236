package at.uibk.dps.dml.node.metadata.rpc;

import at.uibk.dps.dml.node.util.Timestamp;
import at.uibk.dps.dml.node.metadata.command.InvalidationCommand;
import io.vertx.core.Future;

public interface MetadataRpcService {

    Future<Void> invalidate(int remoteVerticleId, Timestamp timestamp, InvalidationCommand command);

    Future<Void> commit(int remoteVerticleId, String key, Timestamp timestamp);

}
