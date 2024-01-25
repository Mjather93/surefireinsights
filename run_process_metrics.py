"""
 Collect performance data using psutil which has cross-platform compatibility.
 Author: Dan Corless
 Version: 0.0.1
 https://psutil.readthedocs.io/en/latest
"""
import argparse
import csv
import sqlite3
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
import process_metrics
from get_report_fk import report_fk


argParser = argparse.ArgumentParser()
argParser.add_argument("-ntm", "--name_to_match", help="list of names to match for process metrics")
args = argParser.parse_args()

csv_file_path = 'C:/Users/corlessd/OneDrive - ESG/Python/surefireinsights/process_metrics.csv'
interval_seconds = 5
name_to_match = 'java|erlsv|sql'

try:
    # execute the collection with multiple threads to speed up the process.
    with ThreadPoolExecutor(max_workers=2) as executor:
        while True:
            executor.submit(process_metrics.ProcessMetrics.collect_and_write_process_metrics_to_db(report_fk=report_fk,
                                                                                                   names_to_match=name_to_match))
            time.sleep(interval_seconds)

# prints a new error message if you cancel the script.
except KeyboardInterrupt:
    print("Monitoring stopped.")
