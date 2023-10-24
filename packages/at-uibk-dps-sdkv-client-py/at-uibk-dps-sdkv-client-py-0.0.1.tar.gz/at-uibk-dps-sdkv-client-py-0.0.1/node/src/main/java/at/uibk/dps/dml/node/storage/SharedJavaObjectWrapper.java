package at.uibk.dps.dml.node.storage;

import at.uibk.dps.dml.client.storage.SharedObjectArgsCodec;
import at.uibk.dps.dml.node.exception.SharedObjectCommandException;
import at.uibk.dps.dml.node.exception.SharedObjectException;
import at.uibk.dps.dml.node.exception.SharedObjectReflectionException;
import org.apache.commons.lang3.reflect.ConstructorUtils;
import org.apache.commons.lang3.reflect.MethodUtils;

import java.io.Serializable;
import java.lang.reflect.InvocationTargetException;

public class SharedJavaObjectWrapper implements SharedObject {

    private static final String SHARED_OBJECTS_PACKAGE_PREFIX = "at.uibk.dps.dml.node.storage.object.";

    private final SharedObjectArgsCodec argsCodec;

    private final Serializable object;

    public SharedJavaObjectWrapper(SharedObjectArgsCodec argsCodec, String objectType, byte[] encodedArgs) throws SharedObjectException {
        this.argsCodec = argsCodec;
        try {
            Object[] args = argsCodec.decode(encodedArgs);
            Class<?> clazz = Class.forName(SHARED_OBJECTS_PACKAGE_PREFIX + objectType);
            this.object = (Serializable) ConstructorUtils.invokeConstructor(clazz, args);
        } catch (ClassNotFoundException | NoSuchMethodException | IllegalAccessException | InstantiationException e) {
            throw new SharedObjectReflectionException("Failed to invoke constructor of class: " + objectType, e);
        } catch (InvocationTargetException e) {
            throw new SharedObjectCommandException(
                    "Failed to invoke constructor of class: " + objectType, e.getCause());
        }
    }

    public byte[] invokeMethod(String methodName, byte[] encodedArgs) throws SharedObjectException {
        try {
            Object[] args = argsCodec.decode(encodedArgs);
            Object result = MethodUtils.invokeMethod(object, methodName, args);
            return argsCodec.encode(new Object[]{result});
        } catch (NoSuchMethodException | IllegalAccessException e) {
            throw new SharedObjectReflectionException("Failed to invoke method: " + methodName, e);
        } catch (InvocationTargetException e) {
            throw new SharedObjectCommandException("Failed to invoke method: " + methodName, e.getCause());
        }
    }
}
