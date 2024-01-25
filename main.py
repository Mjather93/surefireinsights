import subprocess
import datetime
import task_executor
import logging.config
from concurrent.futures import ThreadPoolExecutor
from initialise import scripts


# If it doesn't already exist, create the sqlite database
subprocess.run(["python", "create_sqlite_db.py"])

# # Gather configuration items
report_name = input("What would you like to name this report? ")
while True:
    monitoring_duration_input = input("How long would you like monitoring to run for, in seconds, for this report? ")
    try:
        monitoring_duration = int(monitoring_duration_input)
        break  # Break out of the loop if conversion to int is successful
    except ValueError:
        print("Please enter a valid integer.")

# Input configuration items into the database
subprocess.run(["python", "configure_monitoring.py", '--report_name', report_name,
                '--monitoring_duration', str(monitoring_duration)])

subprocess.run(["python", "get_report_fk.py"])

subprocess.run(["python", "run_system_specs.py"])

time_delta = datetime.timedelta(seconds=float(monitoring_duration))
end_time = (datetime.datetime.now() + datetime.timedelta(seconds=float(monitoring_duration)))
# print(end_time)

# print(scripts)

if 'scripts' in scripts and scripts['scripts'] is not None:
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
else:
    logging.info("No scripts to process.")

subprocess.run(["python", "stop_monitoring.py"])
