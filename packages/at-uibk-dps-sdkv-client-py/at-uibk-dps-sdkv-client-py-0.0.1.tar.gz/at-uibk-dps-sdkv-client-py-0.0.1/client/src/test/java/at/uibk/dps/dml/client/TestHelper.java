package at.uibk.dps.dml.client;

import at.uibk.dps.dml.client.metadata.KeyConfiguration;
import io.vertx.core.CompositeFuture;
import io.vertx.core.Future;
import io.vertx.core.Vertx;
import io.vertx.junit5.VertxTestContext;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;

public class TestHelper {

    public static DmlClient createDmlClient(Vertx vertx, VertxTestContext testContext) {
        DmlClient client = new DmlClient(vertx);

        client.connect(TestConfig.METADATA_HOST, TestConfig.METADATA_PORT)
                .onComplete(testContext.succeedingThenComplete());

        return client;
    }

    @SuppressWarnings("rawtypes")
    public static Future<Void> deleteAllKeys(DmlClient client) {
        return client.getAllConfigurations()
                .compose(configs -> {
                    List<Future> futures = new ArrayList<>();
                    for (Map.Entry<String, KeyConfiguration> config : configs.entrySet()) {
                        futures.add(client.delete(config.getKey()));
                    }
                    return CompositeFuture.join(futures).mapEmpty();
                });
    }

}
