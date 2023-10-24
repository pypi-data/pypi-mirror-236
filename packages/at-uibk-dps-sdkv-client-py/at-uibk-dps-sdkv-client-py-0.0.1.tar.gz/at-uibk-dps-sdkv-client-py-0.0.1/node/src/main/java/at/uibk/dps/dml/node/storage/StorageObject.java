package at.uibk.dps.dml.node.storage;

import at.uibk.dps.dml.node.util.Timestamp;

import java.io.Serializable;

public class StorageObject implements Serializable {

    private final Timestamp timestamp;

    private SharedObject sharedObject;

    private StorageObjectState state;

    private boolean locked;

    private int lockToken;

    public StorageObject(Timestamp timestamp) {
        this.timestamp = timestamp;
    }

    public Timestamp getTimestamp() {
        return timestamp;
    }

    public SharedObject getSharedObject() {
        return sharedObject;
    }

    public void setSharedObject(SharedObject sharedObject) {
        this.sharedObject = sharedObject;
    }

    public boolean isLocked() {
        return locked;
    }

    public void setLocked(boolean locked) {
        this.locked = locked;
    }

    public int getLockToken() {
        return lockToken;
    }

    public void setLockToken(int lockToken) {
        this.lockToken = lockToken;
    }

    public StorageObjectState getState() {
        return state;
    }

    public void setState(StorageObjectState state) {
        this.state = state;
    }

    public void copyFrom(StorageObject other) {
        this.timestamp.setVersion(other.getTimestamp().getVersion());
        this.timestamp.setCoordinatorVerticleId(other.getTimestamp().getCoordinatorVerticleId());
        this.sharedObject = other.getSharedObject();
        this.state = other.getState();
        this.locked = other.isLocked();
        this.lockToken = other.getLockToken();
    }

    @Override
    public String toString() {
        return "StorageObject{" +
                "timestamp=" + timestamp +
                ", sharedObject=" + sharedObject +
                ", state=" + state +
                ", locked=" + locked +
                ", lockToken=" + lockToken +
                '}';
    }
}
