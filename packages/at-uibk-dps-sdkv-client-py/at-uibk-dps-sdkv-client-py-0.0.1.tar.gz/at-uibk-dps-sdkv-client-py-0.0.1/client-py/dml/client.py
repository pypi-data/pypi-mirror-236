import socket
import time
from enum import Enum
from typing import List, Optional, Dict, Any, Union

from dml.exceptions import StorageCommandException, StorageCommandErrorCode, MetadataCommandException, \
    MetadataCommandErrorCode
from dml.metadata.commands import MetadataCreate, MetadataGet, MetadataGetAll, MetadataReconfigure, MetadataDelete
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


class BaseTcpClient:
    def __init__(self, host, port):
        self._host = host
        self._port = port
        self._sock = None
        self._request_counter = 0

    def _receive_bytes(self, n):
        buf = bytearray(n)
        position = 0
        while position < n:
            bytes_read = self._sock.recv_into(memoryview(buf)[position:])
            if not bytes_read:
                raise EOFError
            position += bytes_read
        return ByteBuffer(buf)

    def _request(self, command, statistics=None):
        self._request_counter += 1
        msg_chunks = command.encode(self._request_counter)
        # encode functions can return the message in chunks to avoid expensive copy operations
        # here we simply concatenate the chunks, so this could probably be implemented more efficiently
        msg = b''.join(msg_chunks)
        msg_length = len(msg)
        self._sock.sendall(msg)
        reply_msg_length = \
            self._receive_bytes(FieldLength.MSG_LENGTH_PREFIX.value).get_int(FieldLength.MSG_LENGTH_PREFIX.value)
        reply_buffer = self._receive_bytes(reply_msg_length)
        result = command.decode_reply(reply_buffer)
        if statistics is not None:
            statistics['bytes_sent'] = msg_length
            statistics['bytes_rcv'] = reply_msg_length
        return result

    def connect(self):
        try:
            self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._sock.connect((self._host, self._port))
        except Exception as err:
            print('Failed to connect to server {}:{}'.format(self._host, self._port))
            raise err

    def disconnect(self):
        self._sock.close()


class MetadataClient(BaseTcpClient):
    """
    Metadata Client
    """

    def create(self, key, replicas=None):
        self._request(MetadataCreate(key, replicas))

    def delete(self, key):
        self._request(MetadataDelete(key))

    def get(self, key):
        return self._request(MetadataGet(key))

    def get_all(self):
        return self._request(MetadataGetAll())

    def reconfigure(self, key, replicas):
        self._request(MetadataReconfigure(key, replicas))


class StorageClient(BaseTcpClient):
    """
    Storage Client
    """

    def __init__(self, host, port, shared_object_args_codec=BsonArgsCodec(), statistics=None):
        super().__init__(host, port)
        self.shared_object_args_codec = shared_object_args_codec
        self._statistics = statistics

    def init_object(self, key, object_type, language_id='java', args=None, lock_token=None):
        return self._request(StorageInitObject(self.shared_object_args_codec, key, language_id, object_type, args, lock_token))

    def invoke_method(self, key, method_name, args=None, lock_token=None, flags=CommandFlag.NONE):
        req_statistics = {}
        result = self._request(
            StorageInvokeMethod(self.shared_object_args_codec, key, method_name, args, lock_token, flags),
            statistics=req_statistics
        )
        if self._statistics is not None and flags & CommandFlag.READ_ONLY:
            self._statistics.add_storage_get_req(key, req_statistics['bytes_sent'] + req_statistics['bytes_rcv'])
        elif self._statistics is not None:
            self._statistics.add_storage_set_req(key, req_statistics['bytes_sent'] + req_statistics['bytes_rcv'])
        return result

    def lock(self, key):
        return self._request(StorageLock(key))

    def unlock(self, key, lock_token):
        return self._request(StorageUnlock(key, lock_token))


MAX_RETRIES = 3


class DmlClient:
    """
    DML Client (wrapper for metadata and storage clients)
    """

    def __init__(self, host, port,
                 statistics_writer=None,
                 ap_info_service=AccessPointInfoService(),
                 shared_object_args_codec=BsonArgsCodec(),
                 read_storage_selector=FirstStorageSelector()):
        self.host = host
        self.port = port
        self._statistics = None
        if statistics_writer is not None:
            self._statistics = Statistics(statistics_writer, ap_info_service=ap_info_service)
        self.shared_object_args_codec = shared_object_args_codec
        self._metadata_client = MetadataClient(host, port)
        self._read_storage_selector = read_storage_selector
        self._write_storage_selector = FirstStorageSelector()  # writes always go to the primary replica
        self._storage_clients = {}  # Storage, StorageClient
        self._key_configs_cache = {}  # Key (String), KeyConfiguration

    def _get_or_create_storage_client(self, storage):
        client = self._storage_clients.get(storage)
        if client is None:
            client = StorageClient(storage.host, storage.port,
                                   shared_object_args_codec=self.shared_object_args_codec,
                                   statistics=self._statistics)
            client.connect()
            self._storage_clients[storage] = client
        return client

    def _execute_storage_command(self, key, command, is_read_only=False):
        attempt = 1
        while True:  # retry loop
            # get the configuration for the key
            key_config = self._key_configs_cache.get(key)
            if key_config is None or key_config.replicas == []:
                key_config = self._metadata_client.get(key)
                self._key_configs_cache[key] = key_config
            # select a storage from the candidates
            selected_storage = self._read_storage_selector.select(key_config.replicas) if is_read_only \
                else self._write_storage_selector.select(key_config.replicas)
            # connect to the selected storage
            storage_client = self._get_or_create_storage_client(selected_storage)
            try:
                # execute the command
                metadata_version, result = command(storage_client)
                if metadata_version != key_config.version:
                    # key configuration is outdated, remove it from the cache (the result is still valid)
                    del self._key_configs_cache[key]
                return result
            except StorageCommandException as err:
                retry = False
                if err.num == StorageCommandErrorCode.KEY_DOES_NOT_EXIST.value \
                        or err.num == StorageCommandErrorCode.NOT_RESPONSIBLE.value:
                    # key might have been migrated to other storage nodes,
                    # remove the storage candidates from the cache
                    del self._key_configs_cache[key]
                    retry = attempt < MAX_RETRIES
                if err.num == StorageCommandErrorCode.OBJECT_NOT_INITIALIZED.value and attempt < MAX_RETRIES:
                    # another client might have just created the object but not yet initialized it, wait a bit and retry
                    time.sleep(0.025)
                    retry = True
                if not retry:
                    raise
                attempt += 1

    def connect(self):
        self._metadata_client.connect()

    def disconnect(self):
        for storage, storage_client in list(self._storage_clients.items()):
            storage_client.disconnect()
            del self._storage_clients[storage]
        self._metadata_client.disconnect()
        if self._statistics is not None:
            self._statistics.flush()

    def create(self, key: str, object_type: str = 'SharedBuffer', args: List[Any] = None,
               replicas: Optional[List[int]] = None, ignore_if_exists: bool = True) -> None:
        """
        Creates a shared object.
        :param key: the name of the object
        :param object_type: the type of the object
        :param args: a list of arguments to be provided to the constructor of the object
        :param replicas: the node IDs storing replicas or None if the replicas should be selected automatically
        :param ignore_if_exists: if True, the method does nothing if the key already exists; if False, it fails if the
        key already exists
        """
        if replicas is not None and replicas == []:
            raise ValueError('Replicas cannot be empty')

        try:
            self._metadata_client.create(key, replicas)
        except MetadataCommandException as err:
            if ignore_if_exists and err.num == MetadataCommandErrorCode.KEY_ALREADY_EXISTS.value:
                return
            else:
                raise

        self._execute_storage_command(
            key, lambda storage_client: storage_client.init_object(key, object_type, args=args)
        )

    def get_configuration(self, key: str) -> KeyConfiguration:
        """
        Returns the configuration of the specified key.
        :param key: the key
        :return: the configuration of the key
        """
        return self._metadata_client.get(key)

    def get_all_configurations(self) -> Dict[str, KeyConfiguration]:
        """
        Returns the configuration of all keys.
        :return: a dict mapping keys to their configurations
        """
        return self._metadata_client.get_all()

    def get(self, key: str, allow_invalid_reads: bool = False) -> bytes:
        """
        Returns the value of the object with the given key.
        :param key: the name of the object
        :param allow_invalid_reads: if True, the method may return an invalid (uncommitted) value
        :return: the value of the object
        """
        flags = CommandFlag.READ_ONLY | CommandFlag.ALLOW_INVALID_READS \
            if allow_invalid_reads else CommandFlag.READ_ONLY
        return self.invoke_method(key, 'get', flags=flags)

    def set(self, key: str, value: Union[bytes, bytearray], async_replication: bool = False) -> None:
        """
        Sets the value of the object with the given key.
        :param key: the name of the object
        :param value: the new value of the object
        :param async_replication: if {@code true}, the future may complete before the value has been fully replicated
        """
        flags = CommandFlag.ASYNC_REPLICATION if async_replication else CommandFlag.NONE
        return self.invoke_method(key, 'set', args=[value], flags=flags)

    def invoke_method(self, key: str, method_name: str, args: List[Any] = None,
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
        return self._execute_storage_command(
            key,
            lambda storage_client: storage_client.invoke_method(
                key, method_name, args=args, lock_token=lock_token, flags=flags
            ),
            is_read_only=True if flags & CommandFlag.READ_ONLY else False
        )

    def lock(self, key: str) -> int:
        """
        Locks the object with the given key. Returns a lock token that must be used for all subsequent operations
        on the object and to unlock it.
        :param key: the name of the object to lock
        :return: a lock token
        """
        return self._execute_storage_command(key, lambda storage_client: storage_client.lock(key))

    def unlock(self, key: str, lock_token: int) -> None:
        """
        Unlocks the object with the given key using the given lock token.
        :param key: the name of the object
        :param lock_token: the lock token returned by the lock method
        """
        self._execute_storage_command(key, lambda storage_client: storage_client.unlock(key, lock_token))

    def reconfigure(self, key: str, new_replica_node_ids: List[int] = None) -> None:
        """
        Migrates the object with the given key to the specified replicas.
        :param key: the name of the object
        :param new_replica_node_ids: the node IDs of the new replicas in a list
        """
        if new_replica_node_ids is None or new_replica_node_ids == []:
            raise ValueError('Replica node IDs must not be empty')
        self._metadata_client.reconfigure(key, new_replica_node_ids)
        self._key_configs_cache.pop(key, None)

    def delete(self, key: str) -> None:
        """
        Deletes the object with the given key.
        :param key: the name of the object
        """
        self._metadata_client.delete(key)
        self._key_configs_cache.pop(key, None)
