import sqlite3

# Connect to SQLite database (or create if it doesn't exist)
connection = sqlite3.connect('surefireinsights.db')

# Create a cursor object to execute SQL queries
cursor = connection.cursor()

# Create a table to store your results
cursor.execute('''
    CREATE TABLE IF NOT EXISTS report (
        report_pk INTEGER PRIMARY KEY AUTOINCREMENT,
        report_name TEXT,
        monitoring_duration INT,
        report_start_time TEXT,
        report_end_time TEXT,
        run_hardware_specs TEXT,
        run_perfmon TEXT
    )
''')

cursor.execute('''
   CREATE TABLE IF NOT EXISTS hardware_specs (
        hardware_specs_pk INTEGER PRIMARY KEY AUTOINCREMENT,
        system_name TEXT,
        system_type TEXT,
        system_release_version_major INT,
        system_release_version_minor INT,
        machine_type TEXT,
        processor_type TEXT,
        processor_spec TEXT,
        ip_address TEXT,
        mac_address TEXT,
        report_fk INTEGER,
        CONSTRAINT fk_report
            FOREIGN KEY (report_fk)
            REFERENCES report(report_pk)
    )
''')

# Commit the changes and close the connection
connection.commit()
connection.close()
