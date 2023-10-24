package at.uibk.dps.dml.client.storage.object;

import at.uibk.dps.dml.client.DmlClient;
import at.uibk.dps.dml.client.storage.Flag;
import io.vertx.core.Future;

import java.util.EnumSet;

public class SharedJson {

    private final DmlClient client;
    private final String name;

    public SharedJson(DmlClient client, String name) {
        this.client = client;
        this.name = name;
    }

    /**
     * Sets the JSON document to the given value.
     *
     * @param value the value to be set
     */
    public Future<Void> set(Object value) {
        return client.invokeMethod(name, "set", new Object[]{value}).mapEmpty();
    }

    /**
     * Sets the value at the given path.
     *
     * @param path the JSONPath to the value to be set
     * @param value the value to be set
     */
    public Future<Void> set(String path, Object value) {
        return client.invokeMethod(name, "set", new Object[]{path, value}).mapEmpty();
    }

    /**
     * Returns the JSON document.
     *
     * @return the JSON document
     */
    public Future<Object> get() {
        return client.invokeMethod(name, "get", null, EnumSet.of(Flag.READ_ONLY));
    }

    /**
     * Returns the value at the given path.
     *
     * @param path the JSONPath to the value to be returned
     * @return the value at the given path
     */
    public Future<Object> get(String path) {
        return client.invokeMethod(name, "get", new Object[]{path}, EnumSet.of(Flag.READ_ONLY));
    }

    /**
     * Adds or updates the key with the given value.
     *
     * @param key the key to add or update
     * @param value the value to add or update
     */
    public Future<Void> put(String key, Object value) {
        return client.invokeMethod(name, "put", new Object[]{"$", key, value}).mapEmpty();
    }

    /**
     * Adds or updates the key with the given value at the given path.
     *
     * @param path the JSONPath to the key
     * @param key the key to add or update
     * @param value the value to add or update
     */
    public Future<Void> put(String path, String key, Object value) {
        return client.invokeMethod(name, "put", new Object[]{path, key, value}).mapEmpty();
    }

    /**
     * Adds the given value to the array at the given path.
     *
     * @param path the JSONPath to the array
     * @param value the value to add
     */
    public Future<Void> add(String path, Object value) {
        return client.invokeMethod(name, "add", new Object[]{path, value}).mapEmpty();
    }

    /**
     * Deletes the value at the given path.
     *
     * @param path the JSONPath to the value to be deleted
     */
    public Future<Void> delete(String path) {
        return client.invokeMethod(name, "delete", new Object[]{path}).mapEmpty();
    }
}
