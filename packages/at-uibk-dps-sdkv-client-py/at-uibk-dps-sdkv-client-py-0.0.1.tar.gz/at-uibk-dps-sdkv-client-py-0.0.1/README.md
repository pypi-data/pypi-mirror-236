# distributed-data-layer

## Prerequisites

- Java 11+

----------------------------

## Build and run a DML node using Gradle

1. Adapt the [conf/config.json](conf/config.json) file. You can override the path to the config file by setting
   the `VERTX_CONFIG_PATH` environment variable.

2. Execute the `gradle run` command:
   ```
   VERTX_CONFIG_PATH="../conf/config.json" ./gradlew -p node run
   ```

----------------------------

## Create a fat jar

Execute the `gradle shadowJar` command:

```
./gradlew shadowJar
```
