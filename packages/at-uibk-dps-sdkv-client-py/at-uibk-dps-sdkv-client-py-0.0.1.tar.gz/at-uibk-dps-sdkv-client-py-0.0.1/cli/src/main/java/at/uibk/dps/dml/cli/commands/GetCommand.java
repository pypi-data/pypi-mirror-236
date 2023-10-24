package at.uibk.dps.dml.cli.commands;

import at.uibk.dps.dml.cli.Command;
import at.uibk.dps.dml.client.DmlClient;
import io.vertx.core.cli.CLI;
import io.vertx.core.cli.CommandLine;
import io.vertx.core.cli.annotations.Argument;
import io.vertx.core.cli.annotations.Name;
import io.vertx.core.cli.annotations.Option;

import java.nio.charset.StandardCharsets;

@Name("get")
public class GetCommand extends Command<DmlClient> {

    private String key;

    private Integer lockToken;

    public GetCommand(CLI cli) {
        super(cli);
    }

    @Argument(index = 0, argName = "key")
    public void setKey(String key) {
        this.key = key;
    }

    @Option(argName = "lock-token", longName = "lock-token", shortName = "l")
    public void setLockToken(Integer lockToken) {
        this.lockToken = lockToken;
    }

    @Override
    @SuppressWarnings("java:S106")
    public void execute(CommandLine commandLine, DmlClient client) {
        client.get(key, lockToken)
                .onSuccess(value -> System.out.println(value == null ? "null" : new String(value, StandardCharsets.UTF_8)))
                .onFailure(err -> System.err.println(err.getMessage()));
    }
}
