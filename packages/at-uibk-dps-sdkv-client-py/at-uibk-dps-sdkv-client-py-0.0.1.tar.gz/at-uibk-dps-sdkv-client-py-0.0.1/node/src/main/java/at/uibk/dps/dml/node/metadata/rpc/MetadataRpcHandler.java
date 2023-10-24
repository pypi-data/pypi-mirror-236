package at.uibk.dps.dml.node.metadata.rpc;

import at.uibk.dps.dml.node.util.BufferReader;
import at.uibk.dps.dml.node.util.Timestamp;
import at.uibk.dps.dml.node.exception.*;
import at.uibk.dps.dml.node.metadata.MetadataService;
import at.uibk.dps.dml.node.metadata.command.*;
import io.vertx.core.Handler;
import io.vertx.core.buffer.Buffer;
import io.vertx.core.eventbus.Message;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class MetadataRpcHandler implements Handler<Message<Buffer>> {

    private final Logger logger = LoggerFactory.getLogger(MetadataRpcHandler.class);

    private final MetadataService metadataService;

    public MetadataRpcHandler(MetadataService metadataService) {
        this.metadataService = metadataService;
    }

    @Override
    public void handle(Message<Buffer> message) {
        BufferReader bufferReader = new BufferReader(message.body());
        bufferReader.getByte(); // RPC type (not needed here)
        MetadataRpcType commandType = MetadataRpcType.values()[bufferReader.getByte()];
        switch (commandType) {
            case INVALIDATE:
                handleInvalidationCommand(message, bufferReader);
                break;
            case COMMIT:
                handleValidationCommand(message, bufferReader);
                break;
            default:
                logger.error("Received an unknown RPC command type: {}", commandType);
                replyError(message, new UnknownCommandException("Unknown command type: " + commandType));
        }
    }

    private void handleInvalidationCommand(Message<Buffer> message, BufferReader bufferReader) {
        Timestamp timestamp = readTimestamp(bufferReader);
        InvalidationCommandType commandType = InvalidationCommandType.values()[bufferReader.getByte()];

        InvalidationCommand command;
        switch (commandType) {
            case CREATE:
                command = new CreateCommand();
                break;
            case RECONFIGURE:
                command = new ReconfigureCommand();
                break;
            case DELETE:
                command = new DeleteCommand();
                break;
            default:
                logger.error("Received an unknown invalidation command type: {}", commandType);
                replyError(message, new UnknownCommandException("Unknown invalidation command type: " + commandType));
                return;
        }

        command.decode(bufferReader);

        metadataService.invalidate(timestamp, command)
                .onSuccess(message::reply)
                .onFailure(err -> replyError(message, err));
    }

    private void handleValidationCommand(Message<Buffer> message, BufferReader bufferReader) {
        String key = readKey(bufferReader);
        Timestamp timestamp = readTimestamp(bufferReader);

        metadataService.commit(key, timestamp)
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
            return MetadataRpcErrorType.UNKNOWN_COMMAND.ordinal();
        }
        if (err instanceof KeyDoesNotExistException) {
            return MetadataRpcErrorType.KEY_DOES_NOT_EXIST.ordinal();
        }
        if (err instanceof CommandRejectedException) {
            return MetadataRpcErrorType.REJECTED.ordinal();
        }
        return MetadataRpcErrorType.UNKNOWN_ERROR.ordinal();
    }
}
