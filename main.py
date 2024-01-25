import sqlite3
import subprocess


# If it doesn't already exist, create the sqlite database
subprocess.run(["python", "create_sqlite_db.py"])

# Gather configuration items
report_name = input("What would you like to name this report? ")
monitoring_duration = input("How long would you like monitoring to run for, in seconds, for this report? ")

# Input configuration items into the database
subprocess.run(["python", "configure_monitoring.py", '--report_name', report_name,
               '--monitoring_duration', monitoring_duration])

# Extract the report_pk for this report and store in a variable
# Insert the report and monitoring info into the report table of the sqlite db
connection = sqlite3.connect('surefireinsights.db')
cursor = connection.cursor()
cursor.execute('''
    select max(report_pk) from report
''')
report_pk = cursor.fetchone()[0]
connection.close()

subprocess.run(["python", "run_system_specs.py", '--report_pk', str(report_pk)])



