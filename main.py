import concurrent.futures
import multiprocessing
import subprocess
import datetime
import task_executor
import logging.config
from concurrent.futures import ThreadPoolExecutor
from initialise import scripts
from create_sqlite_db import CreateDb
from configure_monitoring import ConfigureMonitoring
from configure_monitoring import ConfigureMonitoring
from generate_report import GenerateReport
from create_report_dir import GenerateReportDir

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

if __name__ == "__main__":
    end_time = (datetime.datetime.now() + datetime.timedelta(seconds=float(monitoring_duration)))
    end_time_str = end_time.strftime("%Y-%m-%d %H:%M:%S")
    logging.info(f"Monitoring until: {end_time}")
    if 'scripts' in scripts and scripts['scripts'] is not None:
        finished = False
        try:
            pool = concurrent.futures.ThreadPoolExecutor(max_workers=4)
            for script in scripts['scripts']:
                logging.info(script)
                pool.submit(task_executor.ExecuteTasks.execute_script(script, end_time_str))
            logging.info("Tasks have been executed. We will now wait for the monitoring to finish.")
            logging.info(f"End time -> {end_time}.")
            while not finished:
                current_time = datetime.datetime.now()
                if current_time >= end_time:
                    logging.info("Monitoring finished. The data will now be processed.")
                    pool.shutdown(wait=True)
                    finished = True
        except KeyboardInterrupt:
            print("Monitoring cancelled. Stopping.")
        finally:
            pool.shutdown(wait=True)
            subprocess.run(["python", "stop_monitoring.py"])
    else:
        logging.info("No scripts to process.")
        subprocess.run(["python", "stop_monitoring.py"])

# Create report dir
if __name__ == "__main__":
    process_configure_monitoring = multiprocessing.Process(target=GenerateReportDir.create_report_dir(
        report_name))

subprocess.run(["python", "generate_chart.py"])

# Generate report
if __name__ == "__main__":
    process_configure_monitoring = multiprocessing.Process(target=GenerateReport.create_report_files(
        report_name))

# Update report -
if __name__ == "__main__":
    process_configure_monitoring = multiprocessing.Process(target=GenerateReport.update_report(
        report_name))