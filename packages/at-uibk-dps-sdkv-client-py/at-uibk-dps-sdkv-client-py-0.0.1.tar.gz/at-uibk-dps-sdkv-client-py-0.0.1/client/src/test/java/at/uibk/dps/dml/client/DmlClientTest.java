package at.uibk.dps.dml.client;

import at.uibk.dps.dml.client.metadata.MetadataCommandError;
import at.uibk.dps.dml.client.metadata.MetadataCommandErrorType;
import io.vertx.core.Vertx;
import io.vertx.junit5.VertxExtension;
import io.vertx.junit5.VertxTestContext;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;

import static org.junit.jupiter.api.Assertions.*;

@ExtendWith(VertxExtension.class)
class DmlClientTest {

    private DmlClient client;

    @BeforeEach
    void beforeEach(Vertx vertx, VertxTestContext testContext) {
        client = TestHelper.createDmlClient(vertx, testContext);
    }

    @AfterEach
    void afterEach(VertxTestContext testContext) {
        TestHelper.deleteAllKeys(client)
                .compose(v -> client.disconnect())
                .onComplete(testContext.succeedingThenComplete());
    }

    @Test
    void testCreateIsIgnoredIfKeyAlreadyExists(VertxTestContext testContext) {
        String key = "key1";

        client.create(key)
                .compose(v -> client.create(key))
                .onComplete(testContext.succeedingThenComplete());
    }

    @Test
    void testCreateFailsIfKeyExistsAndIgnoreExistingFlagIsNotSet(VertxTestContext testContext) {
        String key = "key2";

        client.create(key)
                .compose(v -> client.create(key, null, "SharedBuffer", null, false))
                .onComplete(testContext.failing(throwable -> {
                    if (throwable instanceof MetadataCommandError) {
                        MetadataCommandError error = (MetadataCommandError) throwable;
                        if (error.getErrorType() == MetadataCommandErrorType.KEY_ALREADY_EXISTS) {
                            testContext.completeNow();
                        }
                    } else {
                        testContext.failNow("Wrong exception or error type");
                    }
                }));
    }

    @Test
    void testInvokeMethod(VertxTestContext testContext) {
        String key = "key3";
        byte[] value = "myValue1".getBytes();

        client.create(key, "SharedBuffer")
                .compose(v -> client.invokeMethod(key, "set", new Object[]{value}))
                .compose(v -> client.invokeMethod(key, "get", null))
                .onComplete(testContext.succeeding(res -> testContext.verify(() -> {
                    assertArrayEquals(value, (byte[]) res);
                    testContext.completeNow();
                })));
    }

    @Test
    void testSetGet(VertxTestContext testContext) {
        String key = "key4";
        byte[] value = "myValue2".getBytes();

        client.create(key)
                .compose(v -> client.set(key, value))
                .compose(v -> client.get(key))
                .onComplete(testContext.succeeding(res -> testContext.verify(() -> {
                    assertArrayEquals(value, res);
                    testContext.completeNow();
                })));
    }

    @Test
    void testGetFailsAfterDelete(VertxTestContext testContext) {
        String key = "key5";

        client.create(key)
                .compose(v -> client.delete(key))
                .compose(v -> client.get(key))
                .onComplete(testContext.failing(throwable -> {
                    if (throwable instanceof MetadataCommandError) {
                        MetadataCommandError error = (MetadataCommandError) throwable;
                        if (error.getErrorType() == MetadataCommandErrorType.KEY_DOES_NOT_EXIST) {
                            testContext.completeNow();
                        }
                    } else {
                        testContext.failNow("Wrong exception or error type");
                    }
                }));
    }

    @Test
    void testGetAllConfigurations(VertxTestContext testContext) {
        String key1 = "key1";
        String key2 = "key2";

        client.create(key1)
                .compose(v -> client.create(key2))
                .compose(v -> client.getAllConfigurations())
                .onComplete(testContext.succeeding(configs -> testContext.verify(() -> {
                    assertEquals(2, configs.size());
                    assertTrue(configs.containsKey(key1));
                    assertTrue(configs.containsKey(key2));
                    testContext.completeNow();
                })));
    }
}
