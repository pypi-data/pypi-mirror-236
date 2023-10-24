package at.uibk.dps.dml.node.storage.rpc;

import at.uibk.dps.dml.node.util.BufferReader;
import at.uibk.dps.dml.node.util.Timestamp;
import at.uibk.dps.dml.node.exception.*;
import at.uibk.dps.dml.node.storage.StorageService;
import at.uibk.dps.dml.node.storage.command.*;
import io.vertx.core.Handler;
import io.vertx.core.buffer.Buffer;
import io.vertx.core.eventbus.Message;
import org.apache.commons.lang3.SerializationUtils;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class StorageRpcHandler implements Handler<Message<Buffer>> {

    private final Logger logger = LoggerFactory.getLogger(StorageRpcHandler.class);

    private final StorageService storageService;

    public StorageRpcHandler(StorageService storageService) {
        this.storageService = storageService;
    }

    @Override
    public void handle(Message<Buffer> message) {
        BufferReader bufferReader = new BufferReader(message.body());
        bufferReader.getByte(); // RPC type (not needed here)
        StorageRpcType commandType = StorageRpcType.values()[bufferReader.getByte()];
        switch (commandType) {
            case INVALIDATE:
                handleInvalidationCommand(message, bufferReader);
                break;
            case COMMIT:
                handleCommitCommand(message, bufferReader);
                break;
            case GET_OBJECT:
                handleGetObjectCommand(message, bufferReader);
                break;
            default:
                logger.error("Received an unknown RPC command type: {}", commandType);
                replyError(message, new UnknownCommandException("Unknown command type: " + commandType));
        }
    }

    private void handleInvalidationCommand(Message<Buffer> message, BufferReader bufferReader) {
        int originVerticleId = bufferReader.getInt();
        Timestamp timestamp = readTimestamp(bufferReader);
        InvalidationCommandType commandType = InvalidationCommandType.values()[bufferReader.getByte()];

        InvalidationCommand command;
        switch (commandType) {
            case STATE_REPLICATION:
                command = new StateReplicationCommand();
                break;
            case LOCK:
                command = new LockCommand();
                break;
            case UNLOCK:
                command = new UnlockCommand();
                break;
            case INIT_OBJECT:
                command = new InitObjectCommand();
                break;
            case INVOKE_METHOD:
                command = new InvokeMethodCommand();
                break;
            default:
                logger.error("Received an unknown invalidation command type: {}", commandType);
                replyError(message, new UnknownCommandException("Unknown invalidation command type: " + commandType));
                return;
        }

        command.decode(bufferReader);

        storageService.invalidate(originVerticleId, timestamp, command)
                .onSuccess(message::reply)
                .onFailure(err -> replyError(message, err));
    }

    private void handleCommitCommand(Message<Buffer> message, BufferReader bufferReader) {
        int originVerticleId = bufferReader.getInt();
        String key = readKey(bufferReader);
        Timestamp timestamp = readTimestamp(bufferReader);

        storageService.commit(originVerticleId, key, timestamp)
                .onSuccess(message::reply)
                .onFailure(err -> replyError(message, err));
    }

    private void handleGetObjectCommand(Message<Buffer> message, BufferReader bufferReader) {
        bufferReader.getInt(); // skip originVerticleId (not needed here)
        String key = readKey(bufferReader);

        storageService.getObject(key)
                .map(storageObject -> Buffer.buffer(SerializationUtils.serialize(storageObject)))
                .onSuccess(message::reply)
                .onFailure(err -> replyError(message, err));
    }

    private String readKey(BufferReader bufferReader) {
        int keyLength = bufferReader.getInt();
        return bufferReader.getString(keyLength);
    }

    private Timestamp readTimestamp(BufferReader bufferReader) {
        long timestampVersion = bufferReader.getLong();
        int timestampVerticleId = bufferReader.getInt();
        return new Timestamp(timestampVersion, timestampVerticleId);
    }

    private void replyError(Message<Buffer> message, Throwable err) {
        message.fail(encodeException(err), err.getMessage());
    }

    private int encodeException(Throwable err) {
        if (err instanceof UnknownCommandException) {
            return StorageRpcErrorType.UNKNOWN_COMMAND.ordinal();
        }
        if (err instanceof MissingMessagesException) {
            return StorageRpcErrorType.MISSING_MESSAGES.ordinal();
        }
        if (err instanceof ConflictingTimestampsException) {
            return StorageRpcErrorType.CONFLICTING_TIMESTAMPS.ordinal();
        }
        if (err instanceof CommandRejectedException) {
            return StorageRpcErrorType.REJECTED.ordinal();
        }
        if (err instanceof KeyDoesNotExistException) {
            return StorageRpcErrorType.KEY_DOES_NOT_EXIST.ordinal();
        }
        if (err instanceof ObjectNotReadyException) {
            return StorageRpcErrorType.OBJECT_NOT_READY.ordinal();
        }
        return StorageRpcErrorType.UNKNOWN_ERROR.ordinal();
    }
}
