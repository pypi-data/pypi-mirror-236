package at.uibk.dps.dml.node.storage.command;

import at.uibk.dps.dml.client.util.BufferUtil;
import at.uibk.dps.dml.node.util.BufferReader;
import io.vertx.core.Promise;
import io.vertx.core.buffer.Buffer;

public abstract class InvalidationCommand extends Command {

    protected int originVerticleId;

    protected boolean asyncReplication;

    protected InvalidationCommand() {
    }

    protected InvalidationCommand(Promise<Object> promise, String key, Integer lockToken, boolean readOnly,
                                  boolean allowInvalidReads,
                                  int originVerticleId, boolean asyncReplication) {
        super(promise, key, lockToken, readOnly, allowInvalidReads);
        this.originVerticleId = originVerticleId;
        this.asyncReplication = asyncReplication;
    }

    public int getOriginVerticleId() {
        return originVerticleId;
    }

    public boolean isAsyncReplicationEnabled() {
        return asyncReplication;
    }

    public abstract InvalidationCommandType getType();

    public final void encode(Buffer buffer) {
        BufferUtil.appendLengthPrefixedString(buffer, key);
        buffer.appendInt(originVerticleId);
        encodePayload(buffer);
    }

    public final void decode(BufferReader bufferReader) {
        key = bufferReader.getLengthPrefixedString();
        originVerticleId = bufferReader.getInt();
        decodePayload(bufferReader);
    }

    protected abstract void encodePayload(Buffer buffer);

    protected abstract void decodePayload(BufferReader buffer);

}
