package at.uibk.dps.dml.node.storage;

import at.uibk.dps.dml.client.storage.SharedObjectArgsCodec;
import at.uibk.dps.dml.node.exception.SharedObjectException;

public class SharedObjectFactoryImpl implements SharedObjectFactory {

    protected final SharedObjectArgsCodec argsCodec;

    public SharedObjectFactoryImpl(SharedObjectArgsCodec argsCodec) {
        this.argsCodec = argsCodec;
    }

    @Override
    public SharedObject createObject(String languageId, String objectType, byte[] encodedArgs) throws SharedObjectException {
        if (languageId.equals("java")) {
            return new SharedJavaObjectWrapper(argsCodec, objectType, encodedArgs);
        }
        throw new IllegalArgumentException("Language not supported: " + languageId);
    }
}
