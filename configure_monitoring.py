import argparse
from datetime import datetime
from os import system, name
import sqlite3
import logging_config


def clear_console():
    # for windows
    if name == 'nt':
        _ = system('cls')

    # for mac and linux
    else:
        _ = system('clear')


# Import logging configuration
logging_config.logging_config()

# Import args
argParser = argparse.ArgumentParser()
argParser.add_argument("-rn", "--report_name", help="Path to the config.yaml file")
argParser.add_argument("-md", "--monitoring_duration", help="Path to the config.yaml file")
args = argParser.parse_args()

report_name = args.report_name
monitoring_duration = float(args.monitoring_duration)

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
    (report_name, monitoring_duration, monitoring_start_time)
    VALUES (?, ?, ?)
''', (report_name, monitoring_duration, monitoring_start_time))
connection.commit()
cursor.close()
connection.close()
report_pk = cursor.lastrowid
