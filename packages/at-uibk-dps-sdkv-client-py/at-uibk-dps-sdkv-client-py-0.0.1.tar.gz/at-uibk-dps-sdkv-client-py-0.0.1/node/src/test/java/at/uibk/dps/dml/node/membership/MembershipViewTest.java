package at.uibk.dps.dml.node.membership;

import org.junit.jupiter.api.Test;

import java.util.Collections;
import java.util.List;
import java.util.Map;
import java.util.Set;

import static org.junit.jupiter.api.Assertions.assertEquals;

class MembershipViewTest {

    @Test
    void testFindVerticleById() {
        DmlNodeInfo node1 = new DmlNodeInfo("region", "hostname", 1, false, null);
        VerticleInfo verticle1 = new VerticleInfo(1, VerticleType.METADATA, 9000, node1);
        VerticleInfo verticle2 = new VerticleInfo(2, VerticleType.STORAGE, 9001, node1);
        VerticleInfo verticle3 = new VerticleInfo(3, VerticleType.STORAGE, 9002, node1);
        node1.setVerticles(List.of(verticle1, verticle2, verticle3));
        DmlNodeInfo node2 = new DmlNodeInfo("region", "hostname", 1, false, null);
        VerticleInfo verticle4 = new VerticleInfo(4, VerticleType.STORAGE, 9000, node2);
        node2.setVerticles(Collections.singletonList(verticle4));
        MembershipView view = new MembershipView(1, Map.of("node1", node1, "node2", node2));

        assertEquals(verticle1, view.findVerticleById(1));
        assertEquals(verticle2, view.findVerticleById(2));
        assertEquals(verticle3, view.findVerticleById(3));
        assertEquals(verticle4, view.findVerticleById(4));
    }

    @Test
    void testGetVerticleIdsByType() {
        DmlNodeInfo node1 = new DmlNodeInfo("region", "hostname", 1, false, null);
        VerticleInfo verticle1 = new VerticleInfo(1, VerticleType.METADATA, 9000, node1);
        VerticleInfo verticle2 = new VerticleInfo(2, VerticleType.STORAGE, 9001, node1);
        VerticleInfo verticle3 = new VerticleInfo(3, VerticleType.STORAGE, 9002, node1);
        node1.setVerticles(List.of(verticle1, verticle2, verticle3));
        DmlNodeInfo node2 = new DmlNodeInfo("region", "hostname", 1, false, null);
        VerticleInfo verticle4 = new VerticleInfo(4, VerticleType.STORAGE, 9000, node2);
        node2.setVerticles(Collections.singletonList(verticle4));
        MembershipView view = new MembershipView(1, Map.of("node1", node1, "node2", node2));

        assertEquals(Collections.singleton(verticle1.getId()), view.getVerticleIdsByType(VerticleType.METADATA));
        assertEquals(Set.of(verticle2.getId(), verticle3.getId(), verticle4.getId()),
                view.getVerticleIdsByType(VerticleType.STORAGE));
    }
}
