package at.uibk.dps.dml.node.metadata.rpc;

import at.uibk.dps.dml.node.RpcType;
import at.uibk.dps.dml.node.util.Timestamp;
import at.uibk.dps.dml.node.exception.MetadataRpcException;
import at.uibk.dps.dml.node.metadata.command.InvalidationCommand;
import io.vertx.core.AsyncResult;
import io.vertx.core.Future;
import io.vertx.core.Vertx;
import io.vertx.core.buffer.Buffer;
import io.vertx.core.eventbus.Message;
import io.vertx.core.eventbus.ReplyException;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class MetadataRpcServiceImpl implements MetadataRpcService {

    private final Logger logger = LoggerFactory.getLogger(MetadataRpcServiceImpl.class);

    private final Vertx vertx;

    public MetadataRpcServiceImpl(Vertx vertx) {
        this.vertx = vertx;
    }

    @Override
    public Future<Void> invalidate(int remoteVerticleId, Timestamp timestamp, InvalidationCommand command) {
        Buffer buffer = Buffer.buffer();
        buffer.appendByte((byte) RpcType.METADATA.ordinal())
                .appendByte((byte) MetadataRpcType.INVALIDATE.ordinal())
                .appendLong(timestamp.getVersion())
                .appendInt(timestamp.getCoordinatorVerticleId())
                .appendByte((byte) command.getType().ordinal());

        command.encode(buffer);

        return vertx.eventBus()
                .<Void>request(String.valueOf(remoteVerticleId), buffer)
                .transform(this::transformRequestResult);
    }

    @Override
    public Future<Void> commit(int remoteVerticleId, String key, Timestamp timestamp) {
        Buffer buffer = Buffer.buffer();
        buffer.appendByte((byte) RpcType.METADATA.ordinal())
                .appendByte((byte) MetadataRpcType.COMMIT.ordinal())
                .appendInt(key.length())
                .appendString(key)
                .appendLong(timestamp.getVersion())
                .appendInt(timestamp.getCoordinatorVerticleId());
        return vertx.eventBus()
                .<Void>request(String.valueOf(remoteVerticleId), buffer)
                .transform(this::transformRequestResult);
    }

    private <T> Future<T> transformRequestResult(AsyncResult<Message<T>> res) {
        if (res.succeeded()) {
            // Return the body of the message
            return Future.succeededFuture(res.result().body());
        } else {
            logger.error("Metadata RPC failed", res.cause());

            // Transform the ReplyException to a MetadataRpcException
            ReplyException replyException = (ReplyException) res.cause();
            MetadataRpcErrorType errorType;
            switch (replyException.failureType()) {
                case RECIPIENT_FAILURE:
                    errorType = MetadataRpcErrorType.values()[replyException.failureCode()];
                    break;
                case TIMEOUT:
                    errorType = MetadataRpcErrorType.TIMEOUT;
                    break;
                case NO_HANDLERS:
                default:
                    errorType = MetadataRpcErrorType.UNKNOWN_ERROR;
                    break;
            }
            return Future.failedFuture(new MetadataRpcException(errorType, replyException.getMessage()));
        }
    }
}
