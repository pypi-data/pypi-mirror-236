package at.uibk.dps.dml.node.storage;

import at.uibk.dps.dml.node.RpcRouter;
import at.uibk.dps.dml.node.membership.MembershipManager;
import at.uibk.dps.dml.node.membership.VerticleInfo;
import at.uibk.dps.dml.node.metadata.MetadataService;
import at.uibk.dps.dml.node.metadata.rpc.MetadataRpcHandler;
import at.uibk.dps.dml.node.metadata.rpc.MetadataRpcService;
import at.uibk.dps.dml.node.metadata.rpc.MetadataRpcServiceImpl;
import at.uibk.dps.dml.node.storage.rpc.*;
import io.vertx.core.AbstractVerticle;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class StorageServerVerticle extends AbstractVerticle {

    private final Logger logger = LoggerFactory.getLogger(StorageServerVerticle.class);

    private final MembershipManager membershipManager;

    private final VerticleInfo verticleInfo;

    private final SharedObjectFactory sharedObjectFactory;

    public StorageServerVerticle(MembershipManager membershipManager, VerticleInfo verticleInfo,
                                 SharedObjectFactory sharedObjectFactory) {
        this.membershipManager = membershipManager;
        this.verticleInfo = verticleInfo;
        this.sharedObjectFactory = sharedObjectFactory;
    }

    @Override
    public void start() {
        MetadataRpcService metadataRpcService = new MetadataRpcServiceImpl(vertx);
        MetadataService metadataService = new MetadataService(vertx, membershipManager,
                verticleInfo, metadataRpcService, null);
        MetadataRpcHandler metadataRpcHandler = new MetadataRpcHandler(metadataService);
        StorageRpcService storageRpcService = new StorageRpcServiceImpl(vertx, verticleInfo.getId());
        StorageService storageService = new StorageService(
                vertx, verticleInfo.getId(),
                sharedObjectFactory,
                storageRpcService, metadataService);
        StorageRpcHandler storageRpcHandler = new StorageRpcHandler(storageService);
        vertx.eventBus().consumer(String.valueOf(verticleInfo.getId()), new RpcRouter(metadataRpcHandler, storageRpcHandler))
                .completionHandler(res -> {
                    if (res.succeeded()) {
                        logger.info("Eventbus registration of verticle {} has reached all nodes", verticleInfo.getId());
                    } else {
                        logger.error("Eventbus registration of verticle {} failed", verticleInfo.getId(), res.cause());
                    }
                });

        vertx.createNetServer()
                .connectHandler(new TcpRequestHandler(storageService, metadataService))
                .listen(verticleInfo.getPort())
                .onSuccess(netServer -> logger.info("Storage server {} is now listening to port {}", verticleInfo.getId(), verticleInfo.getPort()))
                .onFailure(err -> logger.error("Storage server {} failed to bind to port {}", verticleInfo.getId(), verticleInfo.getPort(), err));
    }
}
