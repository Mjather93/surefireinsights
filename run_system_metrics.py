"""
 Collect performance data using psutil which has cross-platform compatibility.
 Author: Dan Corless
 Version: 0.0.1
 https://psutil.readthedocs.io/en/latest
"""
import time
from concurrent.futures import ThreadPoolExecutor
import system_metrics


csv_file_path = 'C:/Users/corlessd/OneDrive - ESG/Python/surefireinsights/metrics.csv'
interval_seconds = 5
report_fk = 1

try:
    # execute the collection with multiple threads to speed up the process.
    with ThreadPoolExecutor(max_workers=2) as executor:
        while True:
            executor.submit(system_metrics.SystemMetrics.collect_and_write_system_metrics_to_db(report_fk))
            time.sleep(interval_seconds)
# prints a new error message if you cancel the script.
except KeyboardInterrupt:
    print("Monitoring stopped.")
