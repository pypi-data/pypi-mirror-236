import asyncio
from asyncio import Task
from enum import Enum
from typing import Dict, Optional, List, Any, Union

from dml.exceptions import StorageCommandException, StorageCommandErrorCode, MetadataCommandException, \
    MetadataCommandErrorCode
from dml.metadata.commands import MetadataCreate, MetadataDelete, MetadataGet, MetadataGetAll, MetadataReconfigure
from dml.metadata.metadata import KeyConfiguration
from dml.statistics import Statistics, AccessPointInfoService
from dml.storage.commands import StorageLock, StorageUnlock, StorageInitObject, StorageInvokeMethod, CommandFlag
from dml.storage.objects import BsonArgsCodec
from dml.storage.selectors import FirstStorageSelector
from dml.util.buffer import ByteBuffer


class FieldLength(Enum):
    MSG_LENGTH_PREFIX = 4
    REQUEST_ID = 4
    CMD_TYPE = 1
    RESULT_TYPE = 1
    ERROR_TYPE = 4


class AsyncProtocol(asyncio.Protocol):
    def __init__(self, on_connection_lost):
        self._on_connection_lost = on_connection_lost
        self._transport = None
        self._request_counter = 0
        self._reply_handlers = {}  # maps request IDs to reply handlers
        self._rcv_buffer = bytearray()

    def connection_made(self, transport):
        self._transport = transport

    def request(self, command, statistics=None):
        self._request_counter += 1
        request_id = self._request_counter
        msg_chunks = command.encode(request_id)

        event_loop = asyncio.get_running_loop()
        result_future = event_loop.create_future()

        def reply_handler(reply_msg):
            nonlocal command, result_future, statistics
            if statistics is not None:
                statistics['bytes_rcv'] = len(reply_msg.memory)
            try:
                result = command.decode_reply(reply_msg)
                result_future.set_result(result)
            except Exception as e:
                result_future.set_exception(e)

        self._reply_handlers[request_id] = reply_handler
        self._transport.writelines(msg_chunks)
        if statistics is not None:
            statistics['bytes_sent'] = sum([len(chunk) for chunk in msg_chunks])
        return result_future

    def data_received(self, data):
        self._rcv_buffer += data
        while True:
            if len(self._rcv_buffer) < FieldLength.MSG_LENGTH_PREFIX.value:
                return  # wait for more data to arrive
            msg_length = int.from_bytes(self._rcv_buffer[:FieldLength.MSG_LENGTH_PREFIX.value],
                                        byteorder='big', signed=True)

            # check whether we have at least one full message in the buffer
            if len(self._rcv_buffer) < FieldLength.MSG_LENGTH_PREFIX.value + msg_length:
                return  # wait for more data to arrive

            # retrieve the first message from the buffer
            msg_start = FieldLength.MSG_LENGTH_PREFIX.value
            msg_end = msg_start + msg_length
            msg, self._rcv_buffer = self._rcv_buffer[msg_start:msg_end], self._rcv_buffer[msg_end:]

            # get the request ID from the message and call the corresponding reply handler
            request_id = int.from_bytes(msg[:FieldLength.REQUEST_ID.value], byteorder='big', signed=True)
            reply_handler = self._reply_handlers.pop(request_id)
            reply_handler(ByteBuffer(msg))

    def connection_lost(self, exc):
        if exc is not None:
            self._transport.close()
        self._on_connection_lost.set_result(True)


class BaseTcpClient:

    def __init__(self, host, port):
        self._host = host
        self._port = port
        self._transport = None
        self._protocol = None
        self.on_connection_lost = None

    async def connect(self):
        event_loop = asyncio.get_running_loop()
        self.on_connection_lost = event_loop.create_future()

        self._transport, self._protocol = await event_loop.create_connection(
            lambda: AsyncProtocol(self.on_connection_lost),
            self._host, self._port
        )

    async def disconnect(self):
        self._transport.close()
        await self.on_connection_lost


class MetadataClient(BaseTcpClient):
    """
    Metadata Client
    """

    async def create(self, key, replicas=None):
        await self._protocol.request(MetadataCreate(key, replicas))

    async def delete(self, key):
        await self._protocol.request(MetadataDelete(key))

    async def get(self, key):
        return await self._protocol.request(MetadataGet(key))

    async def get_all(self):
        return await self._protocol.request(MetadataGetAll())

    async def reconfigure(self, key, replicas):
        await self._protocol.request(MetadataReconfigure(key, replicas))


class StorageClient(BaseTcpClient):
    """
    Storage Client
    """

    def __init__(self, host, port, shared_object_args_codec=BsonArgsCodec(), statistics=None):
        super().__init__(host, port)
        self.shared_object_args_codec = shared_object_args_codec
        self._statistics = statistics

    async def init_object(self, key, object_type, language_id='java', args=None, lock_token=None):
        return await self._protocol.request(
            StorageInitObject(self.shared_object_args_codec, key, language_id, object_type, args, lock_token)
        )

    async def invoke_method(self, key, method_name, args=None, lock_token=None, flags=CommandFlag.NONE):
        req_statistics = {}
        result = await self._protocol.request(
            StorageInvokeMethod(self.shared_object_args_codec, key, method_name, args, lock_token, flags),
            statistics=req_statistics
        )
        if self._statistics is not None and flags & CommandFlag.READ_ONLY:
            self._statistics.add_storage_get_req(key, req_statistics['bytes_sent'] + req_statistics['bytes_rcv'])
        elif self._statistics is not None:
            self._statistics.add_storage_set_req(key, req_statistics['bytes_sent'] + req_statistics['bytes_rcv'])
        return result

    async def lock(self, key):
        return await self._protocol.request(StorageLock(key))

    async def unlock(self, key, lock_token):
        return await self._protocol.request(StorageUnlock(key, lock_token))


MAX_RETRIES = 3


class DmlClient:
    """
    DML Client (wrapper for metadata and storage clients)
    """

    def __init__(self, host, port,
                 statistics_writer=None,
                 ap_info_service=AccessPointInfoService(),
                 read_storage_selector=FirstStorageSelector()):
        self._host = host
        self._port = port
        self._statistics = None
        if statistics_writer is not None:
            self._statistics = Statistics(statistics_writer, ap_info_service=ap_info_service)
        self._metadata_client = MetadataClient(host, port)
        self._read_storage_selector = read_storage_selector
        self._write_storage_selector = FirstStorageSelector()  # writes always go to the primary replica
        self._storage_clients = {}  # Storage, StorageClient
        self._get_key_config_tasks = {}  # Key (String), Task
        self._key_configs_cache = {}  # Key (String), KeyConfiguration

    async def _get_or_create_storage_client(self, storage):
        client = self._storage_clients.get(storage)
        if client is None:
            client = StorageClient(storage.host, storage.port, statistics=self._statistics)
            await client.connect()
            self._storage_clients[storage] = client
            client.on_connection_lost.add_done_callback(lambda _: self._storage_clients.pop(storage, None))
        return client

    async def _get_and_cache_key_config(self, key):
        key_config = await self._metadata_client.get(key)
        self._key_configs_cache[key] = key_config
        return key_config

    def _schedule_get_and_cache_key_config_task(self, key) -> Task:
        # check if there is already a pending request for the key config
        pending_task = self._get_key_config_tasks.get(key)
        if pending_task is not None:
            return pending_task
        task = asyncio.create_task(self._get_and_cache_key_config(key))
        self._get_key_config_tasks[key] = task
        task.add_done_callback(lambda _: self._get_key_config_tasks.pop(key))
        return task

    async def _get_key_config(self, key):
        cached_key_config = self._key_configs_cache.get(key)
        if cached_key_config is not None:
            return cached_key_config
        return await self._schedule_get_and_cache_key_config_task(key)

    async def _execute_storage_command(self, key, command, is_read_only=False):
        attempt = 1
        while True:  # retry loop
            # get the configuration for the key
            key_config = await self._get_key_config(key)
            # select a storage from the candidates
            selected_storage = self._read_storage_selector.select(key_config.replicas) if is_read_only \
                else self._write_storage_selector.select(key_config.replicas)
            # connect to the selected storage
            storage_client = await self._get_or_create_storage_client(selected_storage)
            try:
                # execute the command
                metadata_version, result = await command(storage_client)
                # besides the result, the response also contains the version of the current key configuration
                # we use it to check if the cached configuration is outdated
                cached_key_config = self._key_configs_cache.get(key)
                if cached_key_config is not None and cached_key_config.version != metadata_version:
                    # remove the configuration from the cache and retrieve the new one in the background
                    del self._key_configs_cache[key]
                    self._schedule_get_and_cache_key_config_task(key)
                return result
            except StorageCommandException as err:
                retry = False
                if err.num == StorageCommandErrorCode.KEY_DOES_NOT_EXIST.value \
                        or err.num == StorageCommandErrorCode.NOT_RESPONSIBLE.value:
                    # key might have been migrated to other storage nodes,
                    # remove the storage candidates from the cache
                    self._key_configs_cache.pop(key, None)
                    retry = attempt < MAX_RETRIES
                if err.num == StorageCommandErrorCode.OBJECT_NOT_INITIALIZED.value and attempt < MAX_RETRIES:
                    # another client might have just created the object but not yet initialized it, wait a bit and retry
                    await asyncio.sleep(0.025)
                    retry = True
                if not retry:
                    raise
                attempt += 1

    async def _disconnect_storage(self, storage):
        await self._storage_clients.get(storage).disconnect()

    async def connect(self):
        await self._metadata_client.connect()

    async def disconnect(self):
        # disconnect from storage servers
        disconnect_tasks = [self._disconnect_storage(storage) for storage in self._storage_clients.keys()]
        # disconnect from metadata server
        disconnect_tasks.append(self._metadata_client.disconnect())
        await asyncio.gather(*disconnect_tasks)
        if self._statistics is not None:
            self._statistics.flush()

    async def create(self, key: str, object_type: str = 'SharedBuffer', args: List[Any] = None,
                     replicas: Optional[List[int]] = None, ignore_if_exists: bool = True) -> None:
        """
        Creates a shared object.
        :param key: the name of the object
        :param object_type: the type of the object
        :param args: the arguments to be provided to the constructor of the object
        :param replicas: the node IDs storing replicas or None if the replicas should be selected automatically
        :param ignore_if_exists: if True, the method does nothing if the key already exists; if False, it fails if the
        key already exists
        """
        if replicas is not None and replicas == []:
            raise ValueError('Replicas cannot be empty')

        try:
            await self._metadata_client.create(key, replicas)
        except MetadataCommandException as err:
            if ignore_if_exists and err.num == MetadataCommandErrorCode.KEY_ALREADY_EXISTS.value:
                return
            else:
                raise

        await self._execute_storage_command(
            key, lambda storage_client: storage_client.init_object(key, object_type, args=args)
        )

    async def get_configuration(self, key: str) -> KeyConfiguration:
        """
        Returns the configuration of the specified key.
        :param key: the key
        :return: the configuration of the key
        """
        return await self._metadata_client.get(key)

    async def get_all_configurations(self) -> Dict[str, KeyConfiguration]:
        """
        Returns the configuration of all keys.
        :return: a dict mapping keys to their configurations
        """
        return await self._metadata_client.get_all()

    async def get(self, key: str, allow_invalid_reads: bool = False) -> bytes:
        """
        Returns the value of the object with the given key.
        :param key: the name of the object
        :param allow_invalid_reads: if True, the method may return an invalid (uncommitted) value
        :return: the value of the object
        """
        flags = CommandFlag.READ_ONLY | CommandFlag.ALLOW_INVALID_READS \
            if allow_invalid_reads else CommandFlag.READ_ONLY
        return await self.invoke_method(key, 'get', flags=flags)

    async def set(self, key: str, value: Union[bytes, bytearray], async_replication: bool = False) -> None:
        """
        Sets the value of the object with the given key.
        :param key: the name of the object
        :param value: the new value of the object
        :param async_replication: if {@code true}, the future may complete before the value has been fully replicated
        """
        flags = CommandFlag.ASYNC_REPLICATION if async_replication else CommandFlag.NONE
        await self.invoke_method(key, 'set', args=[value], flags=flags)

    async def invoke_method(self, key: str, method_name: str, args: List[Any] = None,
                            lock_token: Optional[int] = None,
                            flags: CommandFlag = CommandFlag.NONE) -> Any:
        """
        Invokes a method on the object with the given key.
        :param key: the name of the object
        :param method_name: the name of the method to invoke
        :param args: a list of arguments to be provided to the method
        :param lock_token: the lock token to be used for the operation or None if no lock token should be used
        :param flags: the flags to be used for the operation
        :return: the result of the method invocation
        """
        return await self._execute_storage_command(
            key,
            lambda storage_client: storage_client.invoke_method(
                key, method_name, args=args, lock_token=lock_token, flags=flags
            ),
            is_read_only=True if flags & CommandFlag.READ_ONLY else False
        )

    async def lock(self, key: str) -> int:
        """
        Locks the object with the given key. Returns a lock token that must be used for all subsequent operations
        on the object and to unlock it. Requests without the lock token will be queued or rejected.
        :param key: the name of the object to lock
        :return: a lock token
        """
        return await self._execute_storage_command(key, lambda storage_client: storage_client.lock(key))

    async def unlock(self, key: str, lock_token: int) -> None:
        """
        Unlocks the object with the given key using the given lock token.
        :param key: the name of the object
        :param lock_token: the lock token returned by the lock method
        """
        await self._execute_storage_command(key, lambda storage_client: storage_client.unlock(key, lock_token))

    async def reconfigure(self, key: str, new_replica_node_ids: List[int] = None) -> None:
        """
        Migrates the object with the given key to the specified replicas.
        :param key: the name of the object
        :param new_replica_node_ids: the node IDs of the new replicas in a list
        """
        if new_replica_node_ids is None or new_replica_node_ids == []:
            raise ValueError('Replica node IDs must be None or non-empty')
        await self._metadata_client.reconfigure(key, new_replica_node_ids)
        self._key_configs_cache.pop(key, None)
        self._schedule_get_and_cache_key_config_task(key)

    async def delete(self, key: str) -> None:
        """
        Deletes the object with the given key.
        :param key: the name of the object
        """
        await self._metadata_client.delete(key)
        self._key_configs_cache.pop(key, None)
