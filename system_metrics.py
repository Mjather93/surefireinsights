import csv
from datetime import datetime
import psutil


class SystemMetrics:
    """
    This class respresents a collection of methods to gather system-level metrics
    using the psutil library.
    """

    @staticmethod
    def get_system_metrics():
        """
        Public function

        Created on: 23-01-2024
        Description: A method that collects system level performance metrics.
        :return:
        """
        return {
            'timestamp': datetime.now(),
            'cpu_percent': psutil.cpu_percent(interval=None),
            'memory_percent': psutil.virtual_memory().percent,
            'disk_percent': psutil.disk_usage('/').percent,
            'disk_read_time': psutil.disk_io_counters().read_time,
            'disk_read_bytes': psutil.disk_io_counters().read_bytes,
            'disk_write_time': psutil.disk_io_counters().write_time,
            'disk_write_bytes': psutil.disk_io_counters().write_bytes,
            'network_bytes_sent': psutil.net_io_counters().bytes_sent,
            'network_bytes_rec': psutil.net_io_counters().bytes_recv,
        }

    # we should change these to insert into the SQLite DB
    @staticmethod
    def write_to_csv(metrics, csv_file):
        with open(csv_file, 'a', newline='') as csvfile:
            fieldnames = metrics.keys()
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            if csvfile.tell() == 0:
                writer.writeheader()
            writer.writerow(metrics)

    @staticmethod
    def collect_and_write_system_metrics(
            csv_file):
        metrics = SystemMetrics.get_system_metrics()
        SystemMetrics.write_to_csv(metrics, csv_file)
