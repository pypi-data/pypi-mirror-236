import sys
import time

from dml.client import DmlClient
from dml.statistics import StatisticsWriterInfluxDB


def main(args):
    statistics_writer = StatisticsWriterInfluxDB(url=args['influxUrl'], username='dml', password='dmldmldml',
                                                 bucket='test', org='dml')
    dml = DmlClient(args['dmlHostname'], args['dmlPort'], statistics_writer=statistics_writer)
    dml.connect()

    key = args['key']
    dml.create(key)

    cnt = 1
    while True:
        operation_type = 'update' if cnt % 2 == 1 else 'read'
        value_size = 1024
        value = bytes(value_size)
        start = time.time()
        if operation_type == 'read':
            _ = dml.get(key)
        elif operation_type == 'update':
            dml.set(key, value)
        print(cnt, operation_type, key, (time.time() - start))
        cnt += 1
        time.sleep(0.1)

    #  dml.disconnect()
    #  statistics_writer.close()


def lambda_handler(event, _):
    return main(event)


if __name__ == '__main__':
    my_key = 'a'
    if len(sys.argv) >= 2:
        my_key = sys.argv[1]
    my_args = {
        'dmlHostname': '10.0.0.1',
        'dmlPort': 9000,
        'influxUrl': 'http://10.0.0.1:8086',
        'key': my_key
    }
    main(my_args)
