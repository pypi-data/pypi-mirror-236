package at.uibk.dps.dml.node.membership;

import com.fasterxml.jackson.annotation.JsonManagedReference;

import java.util.List;

public class DmlNodeInfo {

    private String region = "local";

    private String hostname = "localhost";

    private int defaultNumReplicas = 1;

    private boolean allowReplicasOnTheSameNode = false;

    @JsonManagedReference
    private List<VerticleInfo> verticles;

    public DmlNodeInfo() {
    }

    public DmlNodeInfo(String region, String hostname, int defaultNumReplicas,
                       boolean allowReplicasOnTheSameNode, List<VerticleInfo> verticles) {
        this.region = region;
        this.hostname = hostname;
        this.defaultNumReplicas = defaultNumReplicas;
        this.allowReplicasOnTheSameNode = allowReplicasOnTheSameNode;
        this.verticles = verticles;
    }

    public String getRegion() {
        return region;
    }

    public void setRegion(String region) {
        this.region = region;
    }

    public String getHostname() {
        return hostname;
    }

    public void setHostname(String hostname) {
        this.hostname = hostname;
    }

    public int getDefaultNumReplicas() {
        return defaultNumReplicas;
    }

    public void setDefaultNumReplicas(int defaultNumReplicas) {
        this.defaultNumReplicas = defaultNumReplicas;
    }

    public boolean isAllowReplicasOnTheSameNode() {
        return allowReplicasOnTheSameNode;
    }

    public void setAllowReplicasOnTheSameNode(boolean allowReplicasOnTheSameNode) {
        this.allowReplicasOnTheSameNode = allowReplicasOnTheSameNode;
    }

    public List<VerticleInfo> getVerticles() {
        return verticles;
    }

    public void setVerticles(List<VerticleInfo> verticles) {
        this.verticles = verticles;
    }
}
