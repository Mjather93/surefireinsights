import sqlite3
import subprocess


def get_yes_no_input(question):
    while True:
        user_input = input(f"{question} (Enter 'yes' or 'no'): ").lower()

        if user_input in ('yes', 'no'):
            return user_input
        else:
            print("Invalid input. Please enter 'yes' or 'no.")


# If it doesn't already exist, create the sqlite database
subprocess.run(["python", "create_sqlite_db.py"])

# Gather configuration items
report_name = input("What would you like to name this report? ")
monitoring_duration = input("How long would you like monitoring to run for, in seconds, for this report? ")
monitoring_interval = input("At what frequency would you like metric data to be collected, "
                            "in seconds, for this report? ")
run_system_specs_question = "Do you want to run the System Specification function?"
run_system_specs = get_yes_no_input(run_system_specs_question)
run_system_metrics_question = "Do you want to run the System Metrics function?"
run_system_metrics = get_yes_no_input(run_system_metrics_question)
run_process_metrics_question = "Do you want to run the Process Metrics function?"
run_process_metrics = get_yes_no_input(run_process_metrics_question)

# Input configuration items into the database
subprocess.run(["python", "configure_monitoring.py", '--report_name', report_name,
               '--monitoring_duration', monitoring_duration, '--monitoring_interval', monitoring_interval,
                '--run_system_specs', run_system_specs, '--run_system_metrics', run_system_metrics,
                '--run_process_metrics', run_process_metrics])

# Extract the report_pk for this report and store in a variable
# Insert the report and monitoring info into the report table of the sqlite db
connection = sqlite3.connect('surefireinsights.db')
cursor = connection.cursor()
cursor.execute('''
    select max(report_pk) from report
''')
report_pk = cursor.fetchone()[0]
connection.close()

if run_system_specs == "yes":
    subprocess.run(["python", "system_specs.py", '--report_pk', str(report_pk)])

