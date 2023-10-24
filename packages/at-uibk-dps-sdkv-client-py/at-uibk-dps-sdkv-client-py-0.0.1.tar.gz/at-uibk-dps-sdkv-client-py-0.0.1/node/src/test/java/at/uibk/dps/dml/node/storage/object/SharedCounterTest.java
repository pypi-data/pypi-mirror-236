package at.uibk.dps.dml.node.storage.object;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;

class SharedCounterTest {

    @Test
    void test() {
        SharedCounter counter = new SharedCounter();
        assertEquals(0, counter.get());
        assertEquals(1, counter.increment(1));
        assertEquals(1, counter.get());
        assertEquals(2, counter.increment(1));
        assertEquals(2, counter.get());
        assertEquals(4, counter.increment(2));
        assertEquals(4, counter.get());
    }
}
