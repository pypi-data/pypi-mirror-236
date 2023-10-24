package at.uibk.dps.dml.node.storage.command;

import io.vertx.core.Promise;

public abstract class Command {

    protected final Promise<Object> promise;

    protected String key;

    protected final Integer lockToken;

    protected boolean readOnly;

    protected boolean allowInvalidReads;

    protected Command() {
        this.promise = null;
        this.lockToken = null;
    }

    protected Command(Promise<Object> promise, String key, Integer lockToken, boolean readOnly, boolean allowInvalidReads) {
        this.promise = promise;
        this.key = key;
        this.lockToken = lockToken;
        this.readOnly = readOnly;
        this.allowInvalidReads = allowInvalidReads;
    }

    public Promise<Object> getPromise() {
        return promise;
    }

    public String getKey() {
        return key;
    }

    public Integer getLockToken() {
        return lockToken;
    }

    public boolean isReadOnly() {
        return readOnly;
    }

    public boolean isAllowInvalidReadsEnabled() {
        return allowInvalidReads;
    }

    public abstract Object apply(CommandHandler handler);
}
