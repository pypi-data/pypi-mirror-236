import time
from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS
from dml.client import DmlClient


def reconfigure(metadataclient, key, replicas=None):
    """
    Move replicas and data
    :param key:
    :param replicas:
    :return:
    """
    if replicas is None or replicas == []:
        raise ValueError("Enter a valid value of replicas")
    else:
        metadataclient.reconfigure(key, replicas)


def get_storages(metadataclient, key):
    """Get current storages where k is located in"""
    storages = metadataclient.get(key)
    return storages


if __name__ == '__main__':
    bucket = "test"
    influx_client = InfluxDBClient(url="http://localhost:8086", username="dml", password="dmldmldml", org="dml")

    write_api = influx_client.write_api(write_options=SYNCHRONOUS)
    query_api = influx_client.query_api()

    host = "localhost"
    port = 9000
    dml = DmlClient(host, port)
    dml.connect()

    key = "d"

    dml.create(key, replicas=[9003])
    B = 1
    KB = 1024 * B
    MB = 1024 * KB
    value = 5 * KB
    value_in_bytes = bytes(value)

    start = time.time()
    dml.set(key, value_in_bytes)
    # print("set: "+str(time.time() - start))

    start = time.time()
    dml.get(key)

    # print("get: "+str(time.time() - start))

    delete = False
    if delete:
        start = "1970-01-01T00:00:00Z"
        stop = "2022-12-14T18:00:00Z"
        delete_api = influx_client.delete_api()
        delete_api.delete(start, stop, '_measurement="dml"', bucket=bucket, org='dml')

    write_api.write("test", "dml", {"measurement": "dml", "tags": {"key": key, "ap": "ap2"},
                                     "fields": {"avg_size": 50.0, "get_accesses": 0, "set_accesses": 10}})

    write_api.write("test", "dml", {"measurement": "dml", "tags": {"key": key, "ap": "ap1"},
                                    "fields": {"avg_size": 50.0, "get_accesses": 13, "set_accesses": 1}})

    dml.disconnect()
