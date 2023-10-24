from __future__ import annotations

import time
from typing import Optional, List, Any, Union, TYPE_CHECKING

import bson

from dml.storage.commands import CommandFlag

if TYPE_CHECKING:
    # avoid circular import
    from dml.client import DmlClient

class BsonArgsCodec:
    @staticmethod
    def encode(args: List[Any]) -> bytes:
        # bson.encode requires a mapping type, so we wrap the args in a dict with the indices as keys
        args_dict = {str(k): v for k, v in enumerate(args)}
        return bson.encode(args_dict)

    @staticmethod
    def decode(encoded_args: Union[bytes, bytearray]) -> List[Any]:
        # bson.decode returns a dictionary instead of an array, so we return the values of the dict in a list
        return list(bson.decode(encoded_args).values())


class SharedBuffer:
    def __init__(self, dml: 'DmlClient', key: str, replicas: Optional[List[int]] = None) -> None:
        self.dml = dml
        self.key = key
        self.dml.create(key, object_type='SharedBuffer', replicas=replicas)

    def get(self) -> bytes:
        return self.dml.get(self.key)

    def set(self, value: Union[bytes, bytearray]):
        self.dml.set(self.key, value)


class SharedCounter:
    def __init__(self, dml: 'DmlClient', key: str, replicas: Optional[List[int]] = None) -> None:
        self.dml = dml
        self.key = key
        self.dml.create(key, object_type='SharedCounter', replicas=replicas)

    def get(self) -> int:
        """
        Returns the current value of the counter.
        :return: the current value of the counter
        """
        return self.dml.invoke_method(self.key, 'get', flags=CommandFlag.READ_ONLY)

    def increment(self, delta: int = 1) -> int:
        """
        Increments the counter by the given delta.
        :param delta: the value to increment the counter by
        :return: the new value of the counter
        """
        return self.dml.invoke_method(self.key, 'increment', args=[delta])


class SharedJson:
    def __init__(self, dml: 'DmlClient', key: str, replicas: Optional[List[int]] = None) -> None:
        """
        Creates a new shared JSON document. If a document with the same name already exists, the existing document will
        be used.
        :param dml: the DML client
        :param key: the name of the document
        :param replicas: the node IDs storing replicas or None if the replicas should be selected automatically
        """
        self.dml = dml
        self.key = key
        self.dml.create(key, object_type='SharedJson', replicas=replicas)

    def set(self, value: Any, path: str = '$') -> None:
        """
        Sets the value at the given path.
        :param value: the value to be set
        :param path: the JSONPath to the value to be set
        """
        self.dml.invoke_method(self.key, 'set', args=[path, value])

    def get(self, path: str = '$') -> Any:
        """
        Returns the value at the given path.
        :param path: the JSONPath to the value to be returned
        :return: the value at the given path
        """
        return self.dml.invoke_method(self.key, 'get', args=[path], flags=CommandFlag.READ_ONLY)

    def put(self, key: str, value: Any, path: str = '$') -> None:
        """
        Adds or updates the key with the given value at the given path.
        :param key: the key to add or update
        :param value: the value to add or update
        :param path: the JSONPath to the key
        """
        self.dml.invoke_method(self.key, 'put', args=[path, key, value])

    def add(self, value: Any, path: str = '$') -> None:
        """
        Adds the given value to the array at the given path.
        :param value: the value to add
        :param path: the JSONPath to the array
        """
        self.dml.invoke_method(self.key, 'add', args=[path, value])

    def delete(self, path: str = '$') -> None:
        """
        Deletes the value at the given path.
        :param path: the JSONPath to the value to be deleted
        """
        self.dml.invoke_method(self.key, 'delete', args=[path])

    def stringify(self) -> str:
        """
        Returns a string representation of the JSON document.
        :return: a string representation of the JSON document
        """
        return self.dml.invoke_method(self.key, 'getAsString', flags=CommandFlag.READ_ONLY)


class Barrier:
    def __init__(self, dml: 'DmlClient', key: str, parties: int, replicas: Optional[List[int]] = None,
                 check_delay: float = 0.1) -> None:
        self._dml = dml
        self._key = key
        self._parties = parties
        self._counter = SharedCounter(dml, key, replicas=replicas)
        self._check_delay = check_delay

    def wait(self, timeout: float = None) -> None:
        """
        Waits until all parties have called wait or the specified timeout is reached.
        :param timeout: the timeout in seconds
        """
        self._counter.increment()
        start = time.monotonic()
        while self._counter.get() % self._parties != 0:
            if timeout is not None and time.monotonic() - start > timeout:
                raise TimeoutError('Barrier wait timed out')
            time.sleep(self._check_delay)
