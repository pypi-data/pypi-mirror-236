package at.uibk.dps.dml.node.storage.object;

import java.io.Serializable;

public class SharedString implements Serializable {

    private String string;

    public SharedString() {
    }

    public SharedString(String string) {
        this.string = string;
    }

    public void set(String string) {
        this.string = string;
    }

    public String get() {
        return this.string;
    }
}
