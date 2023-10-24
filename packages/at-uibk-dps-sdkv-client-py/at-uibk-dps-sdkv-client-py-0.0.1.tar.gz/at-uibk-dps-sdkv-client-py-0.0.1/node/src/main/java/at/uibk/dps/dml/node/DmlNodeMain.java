package at.uibk.dps.dml.node;

import at.uibk.dps.dml.client.storage.BsonArgsCodec;
import at.uibk.dps.dml.node.membership.DmlNodeInfo;
import at.uibk.dps.dml.node.membership.MembershipManager;
import at.uibk.dps.dml.node.membership.VerticleInfo;
import at.uibk.dps.dml.node.metadata.MetadataServerVerticle;
import at.uibk.dps.dml.node.storage.SharedObjectFactoryImpl;
import at.uibk.dps.dml.node.storage.StorageServerVerticle;
import io.vertx.config.ConfigRetriever;
import io.vertx.core.Vertx;
import io.vertx.core.VertxOptions;
import io.vertx.core.json.JsonObject;
import io.vertx.ext.cluster.infinispan.InfinispanClusterManager;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class DmlNodeMain {

    private static final Logger logger = LoggerFactory.getLogger(DmlNodeMain.class);

    public static void main(String[] args) {

        // We use a temporary Vert.x instance to retrieve the node configuration
        Vertx tempVertx = Vertx.vertx();
        ConfigRetriever retriever = ConfigRetriever.create(tempVertx);

        retriever.getConfig().onSuccess(config -> {
            tempVertx.close();

            JsonObject nodeInfoJson = config.getJsonObject("nodeInfo");
            DmlNodeInfo nodeInfo = nodeInfoJson.mapTo(DmlNodeInfo.class);
            // Override hostname and number of replicas if specified as system properties
            nodeInfo.setHostname(System.getProperty("dml.hostname", nodeInfo.getHostname()));
            nodeInfo.setDefaultNumReplicas(Integer.getInteger("dml.replicas", nodeInfo.getDefaultNumReplicas()));

            InfinispanClusterManager clusterManager = new InfinispanClusterManager();
            VertxOptions options = new VertxOptions().setClusterManager(clusterManager);
            options.getEventBusOptions().setClusterNodeMetadata(JsonObject.mapFrom(nodeInfo));

            Vertx.clusteredVertx(options)
                    .onSuccess(vertx -> {
                        MembershipManager membershipManager = new MembershipManager(vertx, clusterManager);
                        for (VerticleInfo verticleInfo : nodeInfo.getVerticles()) {
                            switch (verticleInfo.getType()) {
                                case METADATA:
                                    vertx.deployVerticle(new MetadataServerVerticle(membershipManager, verticleInfo));
                                    break;
                                case STORAGE:
                                    vertx.deployVerticle(new StorageServerVerticle(
                                            membershipManager, verticleInfo,
                                            new SharedObjectFactoryImpl(new BsonArgsCodec())));
                                    break;
                                default:
                                    logger.error("Invalid verticle type");
                                    break;
                            }
                        }
                    })
                    .onFailure(throwable -> logger.error("Creation of clustered instance failed", throwable));


        }).onFailure(err -> {
            logger.error("Failed to read the configuration", err);
            tempVertx.close();
        });
    }
}
