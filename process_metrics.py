import csv
from datetime import datetime
import psutil


class ProcessMetrics:
    """
    This class respresents a collection of methods to gather system-level metrics
    using the psutil library.
    """

    @staticmethod
    def get_process_metrics():
        """
        Public function

        Created on: 23-01-2024
        Description: A method that collects system level performance metrics.
        :return:
        """
        processes_data = {}
        process_metrics = psutil.process_iter()
        for processes in process_metrics:
            # print(processes.name())
            processes_data += {
                'timestamp': datetime.now(),
                'process_id': processes.pid,
                'process_name': processes.name(),
                'command_line': processes.cmdline(),
                'cpu_percent': processes.cpu_percent(interval=None),
                'memory_percent': processes.memory_percent(),
                'num_of_threads': processes.threads(),
                'num_of_handles': processes.num_handles(),
                'num_of_open_files': processes.open_files(),
                'io_read_count': processes.io_counters().read_count,
                'io_write_count': processes.io_counters().write_count
            }
        return processes_data

    @staticmethod
    def write_to_csv(metrics, csv_file):
        with open(csv_file, 'a', newline='') as csvfile:
            fieldnames = metrics.keys()
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            if csvfile.tell() == 0:
                writer.writeheader()
            writer.writerow(metrics)

    @staticmethod
    def collect_and_write_process_metrics(
            csv_file):
        metrics = ProcessMetrics.get_process_metrics()
        ProcessMetrics.write_to_csv(metrics, csv_file)
