import csv
import sqlite3
from datetime import datetime
import psutil


class ProcessMetrics:
    """
    This class respresents a collection of methods to gather system-level metrics
    using the psutil library.
    """

    @staticmethod
    def get_process_metrics(names_to_match):
        """
        Public function

        Created on: 23-01-2024
        Description: A method that collects system level performance metrics.
        :return:
        """
        processes_data = {}
        process_metrics = psutil.process_iter()
        for processes in process_metrics:
            if not processes.name() in names_to_match:
                continue
            processes_info = {
                'timestamp': f'{datetime.now()}',
                'process_id': processes.pid,
                'process_name': processes.name(),
                'process_cpu_percent': processes.cpu_percent(interval=None),
                'process_memory_percent': processes.memory_percent(),
                'process_num_of_handles': processes.num_handles(),
                'process_read_count': processes.io_counters().read_count,
                'process_write_count': processes.io_counters().write_count
            }
            try:
                processes_info['process_command_line'] = processes.cmdline()
            except Exception as e:
                processes_info['process_command_line'] = ''
            try:
                processes_info['process_num_of_threads'] = processes.threads()
            except Exception as e:
                processes_info['process_num_of_threads'] = 0
            try:
                processes_info['process_num_of_open_files'] = processes.open_files()
            except Exception as e:
                processes_info['process_num_of_open_files'] = 0

            processes_data[processes.pid] = processes_info
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

    @staticmethod
    def write_to_db(
            metrics,
            report_fk
    ):
        # print(tuple(metrics.values()))
        for processes in metrics.values():
            print(processes.values())
            connection = sqlite3.connect('surefireinsights.db')
            cursor = connection.cursor()
            # return metrics
            cursor.execute('''
                INSERT INTO process_metrics
                (timestamp, process_id, process_name, process_command_line, process_cpu_percent, process_memory_percent,
                process_num_of_threads, process_num_of_handles, process_num_of_open_files, process_read_count,
                process_write_count, report_fk)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', tuple(processes.values()) + (report_fk,))
            connection.commit()
            connection.close()

    @staticmethod
    def collect_and_write_process_metrics_to_db(
            report_fk,
            names_to_match
    ):
        metrics = ProcessMetrics.get_process_metrics(names_to_match)
        ProcessMetrics.write_to_db(metrics, report_fk=report_fk)
