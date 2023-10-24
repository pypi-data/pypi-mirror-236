package at.uibk.dps.dml.client.storage.object;

import at.uibk.dps.dml.client.DmlClient;
import at.uibk.dps.dml.client.TestHelper;
import io.vertx.core.CompositeFuture;
import io.vertx.core.Vertx;
import io.vertx.junit5.VertxExtension;
import io.vertx.junit5.VertxTestContext;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;

import static org.junit.jupiter.api.Assertions.assertEquals;

@ExtendWith(VertxExtension.class)
class SharedCounterTest {

    private DmlClient client;

    @BeforeEach
    void beforeEach(Vertx vertx, VertxTestContext testContext) {
        client = TestHelper.createDmlClient(vertx, testContext);
    }

    @AfterEach
    void afterEach(VertxTestContext testContext) {
        client.disconnect().onComplete(testContext.succeedingThenComplete());
    }

    @Test
    void testGet(VertxTestContext testContext) {
        String key = "counter1";

        client.createSharedCounter(key)
                .compose(SharedCounter::get)
                .onComplete(testContext.succeeding(value -> testContext.verify(() -> {
                    assertEquals(0L, value);
                    testContext.completeNow();
                })));
    }

    @Test
    void testIncrement(VertxTestContext testContext) {
        String key = "counter2";

        client.createSharedCounter(key)
                .onComplete(testContext.succeeding(sharedCounter ->
                        CompositeFuture.all(sharedCounter.increment(), sharedCounter.increment(), sharedCounter.increment())
                                .onComplete(testContext.succeeding(value -> testContext.verify(() -> {
                                    assertEquals(1L, (Long) value.resultAt(0));
                                    assertEquals(2L, (Long) value.resultAt(1));
                                    assertEquals(3L, (Long) value.resultAt(2));
                                    testContext.completeNow();
                                })))
                        )
                );
    }

    @Test
    void testIncrementDeltaArgument(VertxTestContext testContext) {
        String key = "counter3";
        long delta = 5L;

        client.createSharedCounter(key)
                .compose(sharedCounter -> sharedCounter.increment(delta))
                .onComplete(testContext.succeeding(value -> testContext.verify(() -> {
                    assertEquals(delta, value);
                    testContext.completeNow();
                })));
    }
}
