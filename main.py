import multiprocessing
import subprocess
import datetime
import task_executor
import logging.config
from concurrent.futures import ThreadPoolExecutor
from initialise import scripts
from create_sqlite_db import CreateDb
from configure_monitoring import ConfigureMonitoring


# If it doesn't already exist, create the sqlite database
if __name__ == "__main__":
    process_create_db = multiprocessing.Process(target=CreateDb.run_create_db())

# Gather configuration items
report_name = input("What would you like to name this report? ")
while True:
    monitoring_duration_input = input("How long would you like monitoring to run for, in seconds, for this report? ")
    try:
        monitoring_duration = int(monitoring_duration_input)
        break  # Break out of the loop if conversion to int is successful
    except ValueError:
        print("Please enter a valid integer.")

# Input configuration items into the database
if __name__ == "__main__":
    process_configure_monitoring = multiprocessing.Process(target=ConfigureMonitoring.save_config(
        report_name, monitoring_duration))

subprocess.run(["python", "get_report_fk.py"])

subprocess.run(["python", "run_system_specs.py"])

time_delta = datetime.timedelta(seconds=float(monitoring_duration))
end_time = (datetime.datetime.now() + datetime.timedelta(seconds=float(monitoring_duration)))
# print(end_time)

# print(scripts)
logging.info(f"Monitoring until: {end_time}")
if 'scripts' in scripts and scripts['scripts'] is not None:
    try:
        for script in scripts['scripts']:
            logging.info(script)
            task_to_do = task_executor.ExecuteTasks.execute_script(script)
            with ThreadPoolExecutor(max_workers=script['threads']) as executor:
                finished = False
                while not finished:
                    current_time = datetime.datetime.now()
                    if current_time >= end_time:
                        finished = True
                        break
                logging.info("Monitoring finished. The data will now be processed.")
                subprocess.run(["python", "stop_monitoring.py"])
    except KeyboardInterrupt:
        print("Monitoring cancelled. Stopping.")
    finally:
        subprocess.run(["python", "stop_monitoring.py"])
else:
    logging.info("No scripts to process.")
