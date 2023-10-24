package at.uibk.dps.dml.node.storage;

import at.uibk.dps.dml.client.storage.Flag;
import at.uibk.dps.dml.client.util.BufferUtil;
import at.uibk.dps.dml.node.metadata.MetadataEntry;
import at.uibk.dps.dml.node.metadata.MetadataService;
import at.uibk.dps.dml.node.util.BufferReader;
import at.uibk.dps.dml.client.CommandResultType;
import at.uibk.dps.dml.client.storage.StorageCommandErrorType;
import at.uibk.dps.dml.client.storage.StorageCommandType;
import at.uibk.dps.dml.node.exception.*;
import io.vertx.core.Handler;
import io.vertx.core.buffer.Buffer;
import io.vertx.core.net.NetSocket;
import io.vertx.core.parsetools.RecordParser;

import java.util.EnumSet;

public class TcpRequestHandler implements Handler<NetSocket> {

    private final StorageService storageService;
    private final MetadataService metadataService;

    public TcpRequestHandler(StorageService storageService, MetadataService metadataService) {
        this.storageService = storageService;
        this.metadataService = metadataService;
    }

    @Override
    public void handle(NetSocket socket) {
        final RecordParser parser = RecordParser.newFixed(4);
        Handler<Buffer> handler = new Handler<>() {
            boolean readMessageLength = true;

            @Override
            public void handle(Buffer buffer) {
                if (readMessageLength) {
                    readMessageLength = false;
                    parser.fixedSizeMode(buffer.getInt(0));
                } else {
                    readMessageLength = true;
                    parser.fixedSizeMode(4);
                    handleRequest(socket, buffer);
                }
            }
        };
        parser.handler(handler);
        socket.handler(parser);
    }

    private void handleRequest(NetSocket socket, Buffer commandBuffer) {
        BufferReader bufferReader = new BufferReader(commandBuffer);
        int requestId = bufferReader.getInt();
        StorageCommandType commandType = StorageCommandType.valueOf(bufferReader.getByte());
        switch (commandType) {
            case LOCK:
                handleLockCommand(socket, requestId, bufferReader);
                break;
            case UNLOCK:
                handleUnlockCommand(socket, requestId, bufferReader);
                break;
            case INIT_OBJECT:
                handleInitObjectCommand(socket, requestId, bufferReader);
                break;
            case INVOKE_METHOD:
                handleInvokeMethodCommand(socket, requestId, bufferReader);
                break;
            default:
                replyError(socket, requestId, new UnknownCommandException("Unknown command type: " + commandType));
        }
    }

    private void handleLockCommand(NetSocket socket, int requestId, BufferReader bufferReader) {
        String key = bufferReader.getLengthPrefixedString();

        storageService.lock(key)
                .onSuccess(lockToken -> {
                    Buffer replyBuffer = initReplyBufferWithSuccessResultAndMetadataVersion(requestId, key);
                    replyBuffer.appendInt(lockToken);
                    replyBuffer.setInt(0, replyBuffer.length() - 4);
                    socket.write(replyBuffer);
                })
                .onFailure(err -> replyError(socket, requestId, err));
    }

    private void handleUnlockCommand(NetSocket socket, int requestId, BufferReader bufferReader) {
        String key = bufferReader.getLengthPrefixedString();
        int lockToken = bufferReader.getInt();

        storageService.unlock(key, lockToken)
                .onSuccess(res -> replySuccess(socket, requestId, key))
                .onFailure(err -> replyError(socket, requestId, err));
    }

    private void handleInitObjectCommand(NetSocket socket, int requestId, BufferReader bufferReader) {
        String key = bufferReader.getLengthPrefixedString();
        String languageId = bufferReader.getLengthPrefixedString();
        String objectType = bufferReader.getLengthPrefixedString();
        int argsLength = bufferReader.getInt();
        byte[] encodedArgs = argsLength >= 0 ? bufferReader.getBytes(argsLength) : null;

        Integer lockToken = null;
        if (!bufferReader.reachedEnd()) {
            lockToken = bufferReader.getInt();
        }

        storageService.initObject(key, languageId, objectType, encodedArgs, lockToken)
                .onSuccess(res -> replySuccess(socket, requestId, key))
                .onFailure(err -> replyError(socket, requestId, err));
    }

    private void handleInvokeMethodCommand(NetSocket socket, int requestId, BufferReader bufferReader) {
        String key = bufferReader.getLengthPrefixedString();
        String methodName = bufferReader.getLengthPrefixedString();
        int argsLength = bufferReader.getInt();
        byte[] encodedArgs = argsLength >= 0 ? bufferReader.getBytes(argsLength) : null;

        byte flagsBitVector = bufferReader.getByte();
        EnumSet<Flag> flags = EnumSet.noneOf(Flag.class);
        for (Flag flag : Flag.values()) {
            if ((flagsBitVector & flag.getValue()) != 0) {
                flags.add(flag);
            }
        }

        Integer lockToken = null;
        if (!bufferReader.reachedEnd()) {
            lockToken = bufferReader.getInt();
        }

        storageService.invokeMethod(key, methodName, encodedArgs, lockToken, flags)
                .onSuccess(result -> {
                    Buffer replyBuffer = initReplyBufferWithSuccessResultAndMetadataVersion(requestId, key);
                    if (result != null) {
                        replyBuffer.appendInt(result.length).appendBytes(result);
                    } else {
                        replyBuffer.appendInt(-1);
                    }
                    replyBuffer.setInt(0, replyBuffer.length() - 4);
                    socket.write(replyBuffer);
                })
                .onFailure(err -> replyError(socket, requestId, err));
    }

    private int getMetadataVersion(String key) {
        MetadataEntry entry = metadataService.getMetadataEntry(key);
        if (entry == null) {
            return -1;
        }
        return (int) entry.getTimestamp().getVersion();
    }

    private Buffer initReplyBuffer(int requestId, CommandResultType resultType) {
        return Buffer.buffer()
                .appendInt(0) // message length
                .appendInt(requestId)
                .appendByte(resultType.getId());
    }

    private Buffer initReplyBufferWithSuccessResultAndMetadataVersion(int requestId, String key) {
        return initReplyBuffer(requestId, CommandResultType.SUCCESS)
                .appendInt(getMetadataVersion(key));
    }

    private void replySuccess(NetSocket socket, int requestId, String key) {
        Buffer replyBuffer = initReplyBufferWithSuccessResultAndMetadataVersion(requestId, key);
        replyBuffer.setInt(0, replyBuffer.length() - 4);
        socket.write(replyBuffer);
    }

    private void replyError(NetSocket socket, int requestId, Throwable throwable) {
        Buffer replyBuffer = initReplyBuffer(requestId, CommandResultType.ERROR);
        encodeException(replyBuffer, throwable);
        replyBuffer.setInt(0, replyBuffer.length() - 4);
        socket.write(replyBuffer);
    }

    private void encodeException(Buffer replyBuffer, Throwable err) {
        if (err instanceof SharedObjectException) {
            replyBuffer.appendInt(StorageCommandErrorType.SHARED_OBJECT_ERROR.getErrorCode());
            String message = err.getCause().getMessage();
            if (message == null) {
                message = err.getCause().getClass().getName();
            }
            BufferUtil.appendLengthPrefixedString(replyBuffer, message);
            return;
        }
        if (err instanceof UnknownCommandException) {
            replyBuffer.appendInt(StorageCommandErrorType.UNKNOWN_COMMAND.getErrorCode());
        } else if (err instanceof KeyDoesNotExistException) {
            replyBuffer.appendInt(StorageCommandErrorType.KEY_DOES_NOT_EXIST.getErrorCode());
        } else if (err instanceof InvalidLockTokenException) {
            replyBuffer.appendInt(StorageCommandErrorType.INVALID_LOCK_TOKEN.getErrorCode());
        } else if (err instanceof NotResponsibleException) {
            replyBuffer.appendInt(StorageCommandErrorType.NOT_RESPONSIBLE.getErrorCode());
        } else if (err instanceof ObjectNotInitializedException) {
            replyBuffer.appendInt(StorageCommandErrorType.OBJECT_NOT_INITIALIZED.getErrorCode());
        } else {
            replyBuffer.appendInt(StorageCommandErrorType.UNKNOWN_ERROR.getErrorCode());
        }
        replyBuffer.appendInt(-1); // No error message
    }
}
