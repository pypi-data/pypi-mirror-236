package at.uibk.dps.dml.node.storage.rpc;

import at.uibk.dps.dml.node.RpcType;
import at.uibk.dps.dml.node.util.Timestamp;
import at.uibk.dps.dml.node.storage.StorageObject;
import at.uibk.dps.dml.node.storage.command.InvalidationCommand;
import at.uibk.dps.dml.node.exception.StorageRpcException;
import io.vertx.core.AsyncResult;
import io.vertx.core.Future;
import io.vertx.core.Vertx;
import io.vertx.core.buffer.Buffer;
import io.vertx.core.eventbus.Message;
import io.vertx.core.eventbus.ReplyException;
import org.apache.commons.lang3.SerializationUtils;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class StorageRpcServiceImpl implements StorageRpcService {

    private final Logger logger = LoggerFactory.getLogger(StorageRpcServiceImpl.class);

    private final Vertx vertx;

    private final int verticleId;

    public StorageRpcServiceImpl(Vertx vertx, int verticleId) {
        this.vertx = vertx;
        this.verticleId = verticleId;
    }

    @Override
    public Future<Void> invalidate(int remoteVerticleId, Timestamp timestamp, InvalidationCommand command) {
        Buffer buffer = Buffer.buffer();
        buffer.appendByte((byte) RpcType.STORAGE.ordinal())
                .appendByte((byte) StorageRpcType.INVALIDATE.ordinal())
                .appendInt(verticleId)
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
        buffer.appendByte((byte) RpcType.STORAGE.ordinal())
                .appendByte((byte) StorageRpcType.COMMIT.ordinal())
                .appendInt(verticleId)
                .appendInt(key.length())
                .appendString(key)
                .appendLong(timestamp.getVersion())
                .appendInt(timestamp.getCoordinatorVerticleId());
        return vertx.eventBus()
                .<Void>request(String.valueOf(remoteVerticleId), buffer)
                .transform(this::transformRequestResult);
    }

    @Override
    public Future<StorageObject> getObject(int remoteVerticleId, String key) {
        Buffer buffer = Buffer.buffer();
        buffer.appendByte((byte) RpcType.STORAGE.ordinal())
                .appendByte((byte) StorageRpcType.GET_OBJECT.ordinal())
                .appendInt(verticleId)
                .appendInt(key.length())
                .appendString(key);

        return vertx.eventBus()
                .<Buffer>request(String.valueOf(remoteVerticleId), buffer)
                .transform(this::transformRequestResult)
                .map(replyBuffer -> SerializationUtils.deserialize(replyBuffer.getBytes()));
    }

    private <T> Future<T> transformRequestResult(AsyncResult<Message<T>> res) {
        if (res.succeeded()) {
            // Return the body of the message
            return Future.succeededFuture(res.result().body());
        } else {
            logger.error("Storage RPC failed", res.cause());

            // Transform the ReplyException to a StorageRpcException
            ReplyException replyException = (ReplyException) res.cause();
            StorageRpcErrorType errorType;
            switch (replyException.failureType()) {
                case RECIPIENT_FAILURE:
                    errorType = StorageRpcErrorType.values()[replyException.failureCode()];
                    break;
                case TIMEOUT:
                    errorType = StorageRpcErrorType.TIMEOUT;
                    break;
                case NO_HANDLERS:
                default:
                    errorType = StorageRpcErrorType.UNKNOWN_ERROR;
                    break;
            }
            return Future.failedFuture(new StorageRpcException(errorType, replyException.getMessage()));
        }
    }
}

