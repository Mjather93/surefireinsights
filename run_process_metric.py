"""
 Collect performance data using psutil which has cross-platform compatibility.
 Author: Dan Corless
 Version: 0.0.1
 https://psutil.readthedocs.io/en/latest
"""
import time
from concurrent.futures import ThreadPoolExecutor
import process_metrics


csv_file_path = 'C:/Users/corlessd/OneDrive - ESG/Python/surefireinsights/process_metrics.csv'
interval_seconds = 5

try:
    # execute the collection with multiple threads to speed up the process.
    with ThreadPoolExecutor(max_workers=1) as executor:
        while True:
            executor.submit(process_metrics.ProcessMetrics.collect_and_write_process_metrics(csv_file_path))
            time.sleep(interval_seconds)
# prints a new error message if you cancel the script.
except KeyboardInterrupt:
    print("Monitoring stopped. Exported metrics to", csv_file_path)
