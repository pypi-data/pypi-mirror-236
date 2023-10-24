package at.uibk.dps.dml.cli.commands;

import at.uibk.dps.dml.cli.Command;
import at.uibk.dps.dml.client.DmlClient;
import io.vertx.core.cli.CLI;
import io.vertx.core.cli.CommandLine;
import io.vertx.core.cli.annotations.Argument;
import io.vertx.core.cli.annotations.Name;

@Name("delete")
public class DeleteCommand extends Command<DmlClient> {

    private String key;

    public DeleteCommand(CLI cli) {
        super(cli);
    }

    @Argument(index = 0, argName = "key")
    public void setKey(String key) {
        this.key = key;
    }

    @Override
    @SuppressWarnings("java:S106")
    public void execute(CommandLine commandLine, DmlClient client) {
        client.delete(key)
                .onSuccess(res -> System.out.println(getCli().getName() + " successful"))
                .onFailure(err -> System.err.println(err.getMessage()));
    }
}
