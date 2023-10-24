from typing import Any, Optional, List, TYPE_CHECKING

from dml.storage.commands import CommandFlag

if TYPE_CHECKING:
    # avoid circular import
    from dml.asyncio.client import DmlClient


class SharedJson:
    def __init__(self, dml: 'DmlClient', key: str) -> None:
        """
        Creates a proxy object for an existing shared JSON document.
        Use the :func:`dml.asyncio.objects.SharedJson.create` method to create a new shared JSON document.
        :param dml: the DML client
        :param key: the name of the JSON document
        """
        self.dml = dml
        self.key = key

    @classmethod
    async def create(cls, dml: 'DmlClient', key: str, json: Optional[Any] = None,
                     replicas: Optional[List[int]] = None) -> 'SharedJson':
        """
        Creates a new shared JSON document and returns a proxy object for it. If a document with the same name already
        exists, a proxy for the existing document is returned.
        :param dml: the DML client
        :param key: the name of the document
        :param json: the initial content of the JSON document
        :param replicas: the node IDs storing replicas or None if the replicas should be selected automatically
        :return: a proxy object for the JSON document
        """
        self = SharedJson(dml, key)
        await self.dml.create(key, object_type='SharedJson',
                              args=[json] if json is not None else None,
                              replicas=replicas)
        return self

    async def set(self, value: Any, path: str = '$') -> None:
        """
        Sets the value at the given path.
        :param value: the value to be set
        :param path: the JSONPath to the value to be set
        """
        await self.dml.invoke_method(self.key, 'set', args=[path, value])

    async def get(self, path: str = '$') -> Any:
        """
        Returns the value at the given path.
        :param path: the JSONPath to the value to be returned
        :return: the value at the given path
        """
        return await self.dml.invoke_method(self.key, 'get', args=[path], flags=CommandFlag.READ_ONLY)

    async def put(self, key: str, value: Any, path: str = '$') -> None:
        """
        Adds or updates the key with the given value at the given path.
        :param key: the key to add or update
        :param value: the value to add or update
        :param path: the JSONPath to the key
        """
        await self.dml.invoke_method(self.key, 'put', args=[path, key, value])

    async def add(self, value: Any, path: str = '$') -> None:
        """
        Adds the given value to the array at the given path.
        :param value: the value to add
        :param path: the JSONPath to the array
        """
        await self.dml.invoke_method(self.key, 'add', args=[path, value])

    async def delete(self, path: str = '$') -> None:
        """
        Deletes the value at the given path.
        :param path: the JSONPath to the value to be deleted
        """
        await self.dml.invoke_method(self.key, 'delete', args=[path])

    async def stringify(self) -> str:
        """
        Returns a string representation of the JSON document.
        :return: a string representation of the JSON document
        """
        return await self.dml.invoke_method(self.key, 'getAsString', flags=CommandFlag.READ_ONLY)
