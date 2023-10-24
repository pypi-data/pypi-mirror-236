import time

from dml.client import DmlClient


if __name__ == '__main__':
    host = "localhost"
    port = 9000
    dml = DmlClient(host, port)
    dml.connect()

    key = "Hi"
    dml.create(key)
    B = 1
    KB = 1024 * B
    MB = 1024 * KB
    value = 100 * MB
    value_in_bytes = bytes(value)

    start = time.time()
    dml.set(key, value_in_bytes)
    print(time.time() - start)

    dml.disconnect()
