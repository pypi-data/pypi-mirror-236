package at.uibk.dps.dml.node.metadata;

import at.uibk.dps.dml.node.RpcRouter;
import at.uibk.dps.dml.node.membership.MembershipManager;
import at.uibk.dps.dml.node.membership.VerticleInfo;
import at.uibk.dps.dml.node.metadata.rpc.MetadataRpcHandler;
import at.uibk.dps.dml.node.metadata.rpc.MetadataRpcService;
import at.uibk.dps.dml.node.metadata.rpc.MetadataRpcServiceImpl;
import io.vertx.core.AbstractVerticle;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class MetadataServerVerticle extends AbstractVerticle {

    private final Logger logger = LoggerFactory.getLogger(MetadataServerVerticle.class);

    private final MembershipManager membershipManager;

    private final VerticleInfo verticleInfo;

    public MetadataServerVerticle(MembershipManager membershipManager, VerticleInfo verticleInfo) {
        this.membershipManager = membershipManager;
        this.verticleInfo = verticleInfo;
    }

    @Override
    public void start() {
        MetadataRpcService metadataRpcService = new MetadataRpcServiceImpl(vertx);
        StorageMapper storageMapper = verticleInfo.getOwnerNode().isAllowReplicasOnTheSameNode()
                ? new RandomStorageMapper()
                : new NodeAwareRandomStorageMapper();
        MetadataService metadataService = new MetadataService(vertx, membershipManager,
                verticleInfo, metadataRpcService, storageMapper);
        MetadataRpcHandler metadataRpcHandler = new MetadataRpcHandler(metadataService);
        vertx.eventBus().consumer(String.valueOf(verticleInfo.getId()), new RpcRouter(metadataRpcHandler, null))
                .completionHandler(res -> {
                    if (res.succeeded()) {
                        logger.info("Eventbus registration of verticle {} has reached all nodes", verticleInfo.getId());
                    } else {
                        logger.error("Eventbus registration of verticle {} failed", verticleInfo.getId(), res.cause());
                    }
                });

        vertx.createNetServer()
                .connectHandler(new TcpRequestHandler(metadataService))
                .listen(verticleInfo.getPort())
                .onSuccess(netServer -> logger.info("Metadata server {} is now listening to port {}", verticleInfo.getId(), verticleInfo.getPort()))
                .onFailure(err -> logger.error("Metadata server {} failed to bind to port {}", verticleInfo.getId(), verticleInfo.getPort(), err));
    }
}
