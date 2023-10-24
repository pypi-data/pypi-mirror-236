package at.uibk.dps.dml.node.storage.object;

import java.io.Serializable;

public class SharedBuffer implements Serializable {

    private byte[] buffer;

    public SharedBuffer() {
    }

    public SharedBuffer(byte[] buffer) {
        this.buffer = buffer;
    }

    public void set(byte[] buffer) {
        this.buffer = buffer;
    }

    public byte[] get() {
        return this.buffer;
    }
}
