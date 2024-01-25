import sqlite3
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
monitoring_duration = input("How long would you like monitoring to run for, in seconds, for this report? ")

# Input configuration items into the database
subprocess.run(["python", "configure_monitoring.py", '--report_name', report_name,
                '--monitoring_duration', monitoring_duration])

# Extract the report_pk for this report and store in a variable
connection = sqlite3.connect('surefireinsights.db')
cursor = connection.cursor()
cursor.execute('''
    select max(report_pk) from report
''')
report_pk = cursor.fetchone()[0]
connection.close()

subprocess.run(["python", "run_system_specs.py", '--report_pk', str(report_pk)])

time_delta = datetime.timedelta(seconds=float(monitoring_duration))
end_time = (datetime.datetime.now() + datetime.timedelta(seconds=float(monitoring_duration)))
# print(end_time)

print(scripts)

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

subprocess.run(["python", "stop_monitoring.py", '--report_pk', report_pk])
