package at.uibk.dps.dml.client.metadata;

import at.uibk.dps.dml.client.CommandType;

import java.util.Arrays;

public enum MetadataCommandType implements CommandType {

    NONE(0),

    CREATE(1),

    GET(2),

    DELETE(3),

    RECONFIGURE(4),

    GETALL(5);

    private final byte id;

    MetadataCommandType(int id) {
        this.id = (byte) id;
    }

    @Override
    public byte getId() {
        return id;
    }

    public static MetadataCommandType valueOf(int id) {
        return Arrays.stream(MetadataCommandType.values())
                .filter(value -> value.id == id)
                .findFirst()
                .orElse(null);
    }
}
