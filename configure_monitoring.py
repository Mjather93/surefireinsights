import argparse
from datetime import datetime
from os import system, name
import sqlite3
import time
import sys


def clear_console():
    # for windows
    if name == 'nt':
        _ = system('cls')

    # for mac and linux
    else:
        _ = system('clear')


# Import args
argParser = argparse.ArgumentParser()
argParser.add_argument("-rn", "--report_name", help="Path to the config.yaml file")
argParser.add_argument("-md", "--monitoring_duration", help="Path to the config.yaml file")
argParser.add_argument("-mi", "--monitoring_interval", help="Path to the config.yaml file")
argParser.add_argument("-rss", "--run_system_specs", help="Path to the config.yaml file")
argParser.add_argument("-rsm", "--run_system_metrics", help="Path to the config.yaml file")
argParser.add_argument("-rpm", "--run_process_metrics", help="Path to the config.yaml file")
args = argParser.parse_args()

report_name = args.report_name
monitoring_duration = float(args.monitoring_duration)
monitoring_interval = float(args.monitoring_interval)
run_system_specs = args.run_system_specs
run_system_metrics = args.run_system_metrics
run_process_metrics = args.run_process_metrics

# Clear console screen
clear_console()

# Store the monitoring start time
start_datetime = datetime.now()

# Format the date and time as a string
monitoring_start_time = start_datetime.strftime("%Y-%m-%d %H:%M:%S")

# Insert the report and monitoring info into the report table of the sqlite db
connection = sqlite3.connect('surefireinsights.db')
cursor = connection.cursor()
cursor.execute('''
    INSERT INTO report
    (report_name, monitoring_duration, monitoring_interval, monitoring_start_time,
    run_system_specs, run_system_metrics, run_process_metrics)
    VALUES (?, ?, ?, ?, ?, ?, ?)
''', (report_name, monitoring_duration, monitoring_interval, monitoring_start_time,
      run_system_specs, run_system_metrics, run_process_metrics))
connection.commit()
connection.close()
report_pk = cursor.lastrowid

# Run monitoring for duration defined
time.sleep(monitoring_duration)

# Store the monitoring end time
end_datetime = datetime.now()

# Format the date and time as a string
monitoring_end_time = end_datetime.strftime("%Y-%m-%d %H:%M:%S")

# Update report table to add the monitoring end time
connection = sqlite3.connect('surefireinsights.db')
cursor = connection.cursor()
cursor.execute('''
    UPDATE report
    SET monitoring_end_time = ?
    WHERE report_pk = ?
''', (monitoring_end_time, report_pk))
connection.commit()
connection.close()
