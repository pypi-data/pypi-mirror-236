package at.uibk.dps.dml.node.membership;

import io.vertx.core.json.JsonObject;

import java.util.Map;
import java.util.Set;
import java.util.stream.Collectors;

public class MembershipView {

    private final int epoch;

    private final Map<String, DmlNodeInfo> nodeMap;

    public MembershipView(int epoch, Map<String, DmlNodeInfo> nodeMap) {
        this.epoch = epoch;
        this.nodeMap = nodeMap;
    }

    public int getEpoch() {
        return epoch;
    }

    public Map<String, DmlNodeInfo> getNodeMap() {
        return nodeMap;
    }

    public VerticleInfo findVerticleById(int verticleId) {
        return nodeMap.values().stream()
                .flatMap(node -> node.getVerticles().stream())
                .filter(verticleInfo -> verticleInfo.getId() == verticleId)
                .findFirst().orElse(null);
    }

    public Set<Integer> getVerticleIdsByType(VerticleType type) {
        return nodeMap.values().stream()
                .flatMap(node -> node.getVerticles().stream())
                .filter(verticle -> verticle.getType() == type)
                .map(VerticleInfo::getId)
                .collect(Collectors.toSet());
    }

    @Override
    public String toString() {
        return "MembershipView{" +
                "epoch=" + epoch +
                ", nodeMap=" + JsonObject.mapFrom(nodeMap).encodePrettily() +
                '}';
    }
}
