package at.uibk.dps.dml.node.metadata;

import java.util.Set;

public class KeyMetadata {

    private final Set<Integer> objectLocations;

    public KeyMetadata(Set<Integer> objectLocations) {
        this.objectLocations = objectLocations;
    }

    public Set<Integer> getObjectLocations() {
        return objectLocations;
    }
}
