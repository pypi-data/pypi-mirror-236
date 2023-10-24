package at.uibk.dps.dml.node.storage;

import at.uibk.dps.dml.node.util.Timestamp;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;

class StorageObjectTest {

    @Test
    void testCopyFrom() {
        StorageObject obj1 = new StorageObject(new Timestamp(1, 2));
        obj1.setSharedObject((SharedObject) (methodName, encodedArgs) -> new byte[0]);
        obj1.setLocked(true);
        obj1.setLockToken(99);
        obj1.setState(StorageObjectState.VALID);
        StorageObject obj2 = new StorageObject(new Timestamp(0, 0));

        obj2.copyFrom(obj1);

        assertEquals(obj1.getTimestamp(), obj2.getTimestamp());
        assertEquals(obj1.getSharedObject(), obj2.getSharedObject());
        assertEquals(obj1.getState(), obj2.getState());
        assertEquals(obj1.isLocked(), obj2.isLocked());
        assertEquals(obj1.getLockToken(), obj2.getLockToken());
    }
}
