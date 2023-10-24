import time

from dml.client import DmlClient
from dml.statistics import StatisticsWriterInfluxDB


class FakeAccessPointInfoService:
    def __init__(self, current_ap='ap1'):
        self.current_ap = current_ap


def main():
    statistics_writer = StatisticsWriterInfluxDB(url='http://localhost:8086', username='dml', password='dmldmldml',
                                                 bucket='test', org='dml')
    ap_info_service = FakeAccessPointInfoService(current_ap='ap1')
    dml = DmlClient('localhost', 9000, statistics_writer=statistics_writer, ap_info_service=ap_info_service)
    dml.connect()

    key = 'a'
    dml.create(key)

    dml.set(key, bytes(128))
    for _ in range(5):
        dml.get(key)

    time.sleep(1.5)

    for _ in range(10):
        dml.get(key)
        dml.set(key, bytes(1024))

    time.sleep(1.5)

    ap_info_service.current_ap = 'ap3'
    dml.get(key)
    dml.set(key, bytes(512))

    dml.disconnect()
    statistics_writer.close()


if __name__ == '__main__':
    main()
