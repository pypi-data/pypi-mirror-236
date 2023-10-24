package at.uibk.dps.dml.node.storage.command;

public interface CommandHandler {

    Object apply(StateReplicationCommand command);

    Object apply(LockCommand command);

    Object apply(UnlockCommand command);

    Object apply(InitObjectCommand command);

    Object apply(InvokeMethodCommand command);

}
