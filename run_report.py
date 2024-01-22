from datetime import datetime
from os import system, name
import sqlite3
import time


def get_yes_no_input(question):
    while True:
        user_input = input(f"{question} (Enter 'yes' or 'no'): ").lower()

        if user_input in ('yes', 'no'):
            return user_input
        else:
            print("Invalid input. Please enter 'yes' or 'no.")


def clear_console():
    # for windows
    if name == 'nt':
        _ = system('cls')

    # for mac and linux
    else:
        _ = system('clear')


# Ask for the user to choose a report name and store the value in a variable
report_name = input("What would you like to name this report? ")

# Ask for the user to choose a report name and store the value in a variable
monitoring_duration_str = input("How long would you like monitoring to run for, in seconds, for this report? ")
monitoring_duration = float(monitoring_duration_str)

# Ask for the user if they want to run the hardware_stats function and store the value (0 or 1) in a variable
run_hardware_stats_question = "Do you want to run the Hardware Stats function?"
run_hardware_stats = get_yes_no_input(run_hardware_stats_question)

# Ask for the user if they want to run the perfmon function and store the value (0 or 1) in a variable
run_perfmon_question = "Do you want to run the Performance Monitor function?"
run_perfmon = get_yes_no_input(run_perfmon_question)

# Clear console screen
clear_console()

# Store the monitoring start time
start_datetime = datetime.now()

# Format the date and time as a string
report_start_time = start_datetime.strftime("%Y-%m-%d %H:%M:%S")

# Update report table to add the monitoring end time
connection = sqlite3.connect('surefireinsights.db')
cursor = connection.cursor()
cursor.execute('''
    INSERT INTO report (report_name, monitoring_duration, report_start_time, run_hardware_specs, run_perfmon)
    VALUES (?, ?, ?, ?, ?)
''', (report_name, monitoring_duration, report_start_time, run_hardware_stats, run_perfmon))
connection.commit()
connection.close()
report_pk = cursor.lastrowid

# Print the report details
print("Monitoring is due to start for the below configuration")
print(f"Report Name: {report_name}")
print(f"Monitoring Duration: {monitoring_duration}")
print(f"Run Hardware Stats: {run_hardware_stats}")
print(f"Run Performance Monitor: {run_perfmon}")
print(f"Report PK: {report_pk}")
print(f"Monitoring is starting at: {report_start_time}")

# Run monitoring for duration defined
time.sleep(monitoring_duration)

# Store the monitoring end time
end_datetime = datetime.now()

# Format the date and time as a string
report_end_time = end_datetime.strftime("%Y-%m-%d %H:%M:%S")

# Update report table to add the monitoring end time
connection = sqlite3.connect('surefireinsights.db')
cursor = connection.cursor()
cursor.execute('''
    UPDATE report
    SET report_end_time = ?
    WHERE report_pk = ?
''', (report_end_time, report_pk))
connection.commit()
connection.close()

print(f"Monitoring is ending at: {report_end_time}")