package at.uibk.dps.dml.client.storage.object;

import at.uibk.dps.dml.client.DmlClient;
import at.uibk.dps.dml.client.storage.Flag;
import io.vertx.core.Future;

import java.util.EnumSet;

public class SharedCounter {

    private final DmlClient client;
    private final String key;

    public SharedCounter(DmlClient client, String key) {
        this.client = client;
        this.key = key;
    }

    /**
     * Returns the current value of the counter.
     *
     * @return a future that completes with the current value of the counter
     */
    public Future<Long> get() {
        return client.invokeMethod(key, "get", null, EnumSet.of(Flag.READ_ONLY)).map(Long.class::cast);
    }

    /**
     * Increments the counter by 1.
     *
     * @return a future that completes with the new value of the counter
     */
    public Future<Long> increment() {
        return increment(1);
    }

    /**
     * Increments the counter by the given delta.
     *
     * @param delta the value to increment the counter by
     * @return a future that completes with the new value of the counter
     */
    public Future<Long> increment(long delta) {
        return client.invokeMethod(key, "increment", new Object[]{delta}).map(Long.class::cast);
    }
}
