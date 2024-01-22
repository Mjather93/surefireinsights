"""
 Collect performance data using psutil which has cross-platform compatibility.
 Author: Dan Corless
 Version: 0.0.1
 https://psutil.readthedocs.io/en/latest
"""

from datetime import datetime
import csv
import time
import psutil
from concurrent.futures import ThreadPoolExecutor


# pull the metrics we want to collect in via a class/config file.
def collect_metrics():
    return {
        'timestamp': datetime.now(),
        'cpu_percent': psutil.cpu_percent(interval=None),
        'memory_percent': psutil.virtual_memory().percent,
        'disk_percent': psutil.disk_usage('/').percent,
        'network_bytes_sent': psutil.net_io_counters().bytes_sent,
        'network_bytes_rec': psutil.net_io_counters().bytes_recv,
    }


def write_to_csv(metrics, csv_file):
    with open(csv_file, 'a', newline='') as csvfile:
        fieldnames = metrics.keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if csvfile.tell() == 0:
            writer.writeheader()
        writer.writerow(metrics)


def collect_and_write_metrics(csv_file):
    metrics = collect_metrics()
    write_to_csv(metrics, csv_file)


csv_file_path = 'C:/Users/corlessd/OneDrive - ESG/Python/surefireinsights/metrics.csv'
interval_seconds = 5

try:
    # execute the collection with multiple threads to speed up the process.
    with ThreadPoolExecutor(max_workers=2) as executor:
        while True:
            executor.submit(collect_and_write_metrics, csv_file_path)
            time.sleep(interval_seconds)
# prints a new error message if you cancel the script.
except KeyboardInterrupt:
    print("Monitoring stopped. Exported metrics to", csv_file_path)
