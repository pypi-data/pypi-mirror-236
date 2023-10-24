package at.uibk.dps.dml.node.storage.object;

import java.io.Serializable;

public class SharedCounter implements Serializable {

    private long value;

    public long get() {
        return value;
    }

    public long increment(long delta) {
        value += delta;
        return value;
    }
}
