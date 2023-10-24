package at.uibk.dps.dml.node.storage.rpc;

public enum StorageRpcErrorType {

    UNKNOWN_ERROR,

    TIMEOUT,

    UNKNOWN_COMMAND,

    MISSING_MESSAGES,

    CONFLICTING_TIMESTAMPS,

    REJECTED,

    KEY_DOES_NOT_EXIST,

    OBJECT_NOT_READY,
}
