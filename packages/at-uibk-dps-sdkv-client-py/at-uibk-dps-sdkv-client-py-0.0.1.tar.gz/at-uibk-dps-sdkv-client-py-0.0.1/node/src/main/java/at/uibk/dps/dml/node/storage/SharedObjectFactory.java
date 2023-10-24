package at.uibk.dps.dml.node.storage;

import at.uibk.dps.dml.node.exception.SharedObjectException;

public interface SharedObjectFactory {

    SharedObject createObject(String languageId, String objectType, byte[] encodedArgs) throws SharedObjectException;

}
