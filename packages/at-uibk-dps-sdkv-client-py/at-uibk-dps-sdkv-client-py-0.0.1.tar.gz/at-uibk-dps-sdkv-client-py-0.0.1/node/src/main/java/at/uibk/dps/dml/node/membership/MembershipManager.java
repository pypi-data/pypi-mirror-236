package at.uibk.dps.dml.node.membership;

import io.vertx.core.Promise;
import io.vertx.core.Vertx;
import io.vertx.core.spi.cluster.NodeInfo;
import io.vertx.ext.cluster.infinispan.InfinispanClusterManager;
import org.infinispan.manager.EmbeddedCacheManager;
import org.infinispan.notifications.Listener;
import org.infinispan.notifications.cachemanagerlistener.annotation.Merged;
import org.infinispan.notifications.cachemanagerlistener.annotation.ViewChanged;
import org.infinispan.notifications.cachemanagerlistener.event.ViewChangedEvent;
import org.infinispan.remoting.transport.Address;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

public class MembershipManager {

    private final Logger logger = LoggerFactory.getLogger(MembershipManager.class);

    private final Vertx vertx;

    private final InfinispanClusterManager clusterManager;

    private final List<MembershipChangeListener> changeListeners = new ArrayList<>();

    /**
     * Maps node IDs to node infos.
     */
    private final Map<String, DmlNodeInfo> nodeInfoMap = new HashMap<>();

    private final ClusterView ispnClusterView = new ClusterView();

    private MembershipView membershipView = null;

    public MembershipManager(Vertx vertx, InfinispanClusterManager clusterManager) {
        this.vertx = vertx;
        this.clusterManager = clusterManager;
        init();
    }

    private void init() {
        EmbeddedCacheManager ispnCacheManager = (EmbeddedCacheManager) clusterManager.getCacheContainer();
        ispnClusterView.epoch = ispnCacheManager.getTransport().getViewId();
        ispnClusterView.members = ispnCacheManager.getMembers().stream().map(Object::toString).collect(Collectors.toList());
        ispnCacheManager.addListener(new ClusterViewListener());
        ispnClusterView.members.forEach(nodeId -> getNodeInfo(nodeId, System.currentTimeMillis()));
    }

    public void addListener(MembershipChangeListener changeListener) {
        synchronized (changeListeners) {
            changeListeners.add(changeListener);
        }
    }

    public MembershipView getMembershipView() {
        return membershipView;
    }

    @Listener(sync = false)
    private class ClusterViewListener {
        @Merged
        @ViewChanged
        public void handleViewChange(ViewChangedEvent viewChangedEvent) {
            synchronized (this) {
                if (viewChangedEvent.getViewId() <= ispnClusterView.epoch) {
                    return;
                }

                ispnClusterView.epoch = viewChangedEvent.getViewId();
                ispnClusterView.members = viewChangedEvent.getNewMembers().stream().map(Object::toString).collect(Collectors.toList());

                List<Address> addedMembers = new ArrayList<>(viewChangedEvent.getNewMembers());
                addedMembers.removeAll(viewChangedEvent.getOldMembers());
                for (Address addedMember : addedMembers) {
                    getNodeInfo(addedMember.toString(), System.currentTimeMillis());
                }

                List<Address> removedMembers = new ArrayList<>(viewChangedEvent.getOldMembers());
                removedMembers.removeAll(viewChangedEvent.getNewMembers());
                for (Address removedMember : removedMembers) {
                    nodeInfoMap.remove(removedMember.toString());
                }
            }
            checkViewUpdate();
        }
    }

    private void getNodeInfo(String nodeId, long startTime) {
        Promise<NodeInfo> promise = Promise.promise();
        clusterManager.getNodeInfo(nodeId, promise);
        promise.future().onComplete(asyncResult -> {
            if (!ispnClusterView.members.contains(nodeId)) {
                logger.warn("Node {} left while obtaining its metadata", nodeId);
                checkViewUpdate();
                return;
            }
            if (asyncResult.succeeded()) {
                NodeInfo nodeInfo = asyncResult.result();
                if (nodeInfo.metadata() == null) {
                    logger.warn("Node {} joined without metadata", nodeId);
                    return;
                }
                DmlNodeInfo dmlNodeInfo = nodeInfo.metadata().mapTo(DmlNodeInfo.class);
                synchronized (this) {
                    nodeInfoMap.put(nodeId, dmlNodeInfo);
                }
                checkViewUpdate();
            } else {
                // It takes some time until the node info is available after a node joins
                vertx.setTimer(200, timerId -> {
                    if (System.currentTimeMillis() - startTime > 30000) {
                        logger.error("Could not obtain metadata of joined node " + nodeId, asyncResult.cause());
                    } else {
                        getNodeInfo(nodeId, startTime);
                    }
                });
            }
        });
    }

    private void checkViewUpdate() {
        MembershipView newMembershipView;
        synchronized (this) {
            if (!nodeInfoMap.keySet().containsAll(ispnClusterView.members)) {
                return;
            }
            Map<String, DmlNodeInfo> nodeInfoOfMembers = ispnClusterView.members.stream().collect(Collectors.toMap(nodeId -> nodeId, nodeInfoMap::get));
            newMembershipView = new MembershipView(ispnClusterView.epoch, nodeInfoOfMembers);
            membershipView = newMembershipView;
        }

        logger.info("New membership view: {}", newMembershipView);

        synchronized (changeListeners) {
            for (MembershipChangeListener listener : changeListeners) {
                listener.membershipChanged(newMembershipView);
            }
        }
    }

    static class ClusterView {
        int epoch;
        List<String> members;
    }
}
