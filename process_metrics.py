import datetime
import json
import time
import psutil
import multiprocessing
import sqlite3


class ProcessPerformanceExtractor:
    """
    Description:
        A class to extract process-level performance metrics.
        We use a multiprocessing pool to manage the processing of process-level metrics
        across multiple threads.
        Each metric has a method for simplicity.
    """

    def __init__(self, criteria):
        self.criteria = criteria
        self.last_io_counters = {}

    def get_matching_process_ids(self):
        # method to find process IDs that match our process name criteria.
        # we store them in a list to multiprocess the process Ids
        matching_ids = []
        for process in psutil.process_iter(['pid', 'name', 'cmdline']):
            if self.criteria.lower() in process.info['name'].lower():
                matching_ids.append(process.info)
        return matching_ids

    # we need to JSONIFY the cmdline data to store it in the DB.
    def cmdline_to_json(self, cmdline):
        return json.dumps(cmdline)

    def get_current_time(self):
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def get_cpu_usage(self, process_info):
        try:
            process = psutil.Process(process_info['pid'])
            cpu_percent = process.cpu_percent(interval=1)
            return (process_info['pid'], self.get_current_time(), process_info['name'],
                    self.cmdline_to_json(process_info['cmdline']), "cpu_usage_percent", cpu_percent)
        except psutil.NoSuchProcess:
            return (process_info['pid'], self.get_current_time(), process_info['name'],
                    self.cmdline_to_json(process_info['cmdline']), "cpu_usage_percent", 0)

    def get_memory_usage(self, process_info):
        try:
            process = psutil.Process(process_info['pid'])
            memory_info = process.memory_info()
            return (process_info['pid'], self.get_current_time(),
                    process_info['name'],
                    self.cmdline_to_json(process_info['cmdline']), "memory_usage_mb", memory_info.rss / (1024 ** 2))
        except psutil.NoSuchProcess:
            return (process_info['pid'], self.get_current_time(),
                    process_info['name'],
                    self.cmdline_to_json(process_info['cmdline']), "memory_usage_mb", 0)

    def get_io_read_bytes(self, process_info):
        try:
            process = psutil.Process(process_info['pid'])
            io_counters = process.io_counters()
            return (process_info['pid'], self.get_current_time(),
                    process_info['name'],
                    self.cmdline_to_json(process_info['cmdline']), "read_bytes", io_counters.read_bytes)
        except psutil.NoSuchProcess:
            return (process_info['pid'], self.get_current_time(),
                    process_info['name'],
                    self.cmdline_to_json(process_info['cmdline']), "read_bytes", 0)

    def get_io_read_count(self, process_info):
        try:
            process = psutil.Process(process_info['pid'])
            io_counters = process.io_counters()
            return (process_info['pid'], self.get_current_time(),
                    process_info['name'],
                    self.cmdline_to_json(process_info['cmdline']), "read_count", io_counters.read_count)
        except psutil.NoSuchProcess:
            return (process_info['pid'], self.get_current_time(),
                    process_info['name'],
                    self.cmdline_to_json(process_info['cmdline']), "read_count", 0)

    def get_io_write_bytes(self, process_info):
        try:
            process = psutil.Process(process_info['pid'])
            io_counters = process.io_counters()
            return (process_info['pid'], self.get_current_time(),
                    process_info['name'],
                    self.cmdline_to_json(process_info['cmdline']), "write_bytes", io_counters.write_bytes)
        except psutil.NoSuchProcess:
            return (process_info['pid'], self.get_current_time(),
                    process_info['name'],
                    self.cmdline_to_json(process_info['cmdline']), "write_bytes", 0)

    def get_io_write_count(self, process_info):
        try:
            process = psutil.Process(process_info['pid'])
            io_counters = process.io_counters()
            return (process_info['pid'], self.get_current_time(),
                    process_info['name'],
                    self.cmdline_to_json(process_info['cmdline']), "write_count", io_counters.write_count)
        except psutil.NoSuchProcess:
            return (process_info['pid'], self.get_current_time(),
                    process_info['name'],
                    self.cmdline_to_json(process_info['cmdline']), "write_count", 0)

    @staticmethod
    def collect_metrics(process_info, criteria):
        extractor = ProcessPerformanceExtractor(criteria)
        cpu_usage = extractor.get_cpu_usage(process_info)
        memory_usage = extractor.get_memory_usage(process_info)
        read_bytes = extractor.get_io_read_bytes(process_info)
        read_count = extractor.get_io_read_count(process_info)
        write_bytes = extractor.get_io_write_bytes(process_info)
        write_count = extractor.get_io_write_count(process_info)
        return [cpu_usage, memory_usage, read_bytes, read_count, write_bytes, write_count]

    @staticmethod
    def write_to_database(data):
        conn = sqlite3.connect('performance_data.db')
        cursor = conn.cursor()

        for item in data:
            cursor.execute("INSERT INTO process_metrics VALUES (?, ?, ?, ?, ?, ?)", tuple(item))

        conn.commit()
        conn.close()

