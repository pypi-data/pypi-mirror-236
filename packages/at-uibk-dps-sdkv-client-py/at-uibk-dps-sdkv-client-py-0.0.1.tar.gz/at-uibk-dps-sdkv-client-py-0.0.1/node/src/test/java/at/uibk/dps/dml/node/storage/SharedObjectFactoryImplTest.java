package at.uibk.dps.dml.node.storage;

import at.uibk.dps.dml.client.storage.BsonArgsCodec;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.wildfly.common.Assert.assertTrue;

class SharedObjectFactoryImplTest {

    @Test
    void testCreateObject() {
        SharedObjectFactory factory = new SharedObjectFactoryImpl(new BsonArgsCodec());

        assertTrue(factory.createObject("java", "SharedBuffer", null) instanceof SharedJavaObjectWrapper);
    }

    @Test
    void testCreateObjectWithInvalidLanguageThrowsException() {
        SharedObjectFactory factory = new SharedObjectFactoryImpl(new BsonArgsCodec());

        assertThrows(IllegalArgumentException.class, () -> factory.createObject("C+#thon", "SharedBuffer", null));
    }
}
