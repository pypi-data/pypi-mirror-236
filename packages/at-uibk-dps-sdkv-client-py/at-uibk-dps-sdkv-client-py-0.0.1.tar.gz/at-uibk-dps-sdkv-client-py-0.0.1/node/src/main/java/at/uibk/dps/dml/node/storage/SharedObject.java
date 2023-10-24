package at.uibk.dps.dml.node.storage;

import at.uibk.dps.dml.node.exception.SharedObjectException;

import java.io.Serializable;

public interface SharedObject extends Serializable {

    byte[] invokeMethod(String methodName, byte[] encodedArgs) throws SharedObjectException;

}
