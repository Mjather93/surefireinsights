import time
from concurrent.futures import ThreadPoolExecutor
import system_specs


csv_file_path = 'C:/temp/metrics.csv'
report_fk = 1

try:
    system_specs.system_information()
# prints a new error message if you cancel the script.
except KeyboardInterrupt:
    print("Monitoring stopped.")
