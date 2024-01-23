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
        monitoring_duration INTEGER,
        monitoring_interval INTEGER,
        monitoring_start_time TEXT,
        monitoring_end_time TEXT,
        run_system_specs TEXT,
        run_system_metrics TEXT,
        run_process_metrics TEXT
    )
''')

cursor.execute('''
   CREATE TABLE IF NOT EXISTS system_specs (
        system_specs_pk INTEGER PRIMARY KEY AUTOINCREMENT,
        system_name TEXT,
        system_type TEXT,
        system_release_version_major INTEGER,
        system_release_version_minor INTEGER,
        machine_type TEXT,
        processor_type TEXT,
        processor_spec TEXT,
        ip_address TEXT,
        mac_address TEXT,
        last_boot_time TEXT,
        physical_core_count INTEGER,
        total_core_count INTEGER,
        max_core_frequency TEXT,
        total_memory TEXT,
        disk_information TEXT,
        report_fk INTEGER,
        CONSTRAINT fk_report
            FOREIGN KEY (report_fk)
            REFERENCES report(report_pk)
    )
''')

cursor.execute('''
   CREATE TABLE IF NOT EXISTS system_metrics (
        system_metrics_pk INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        cpu_percent INTEGER,
        memory_percent INTEGER,
        disk_percent INTEGER,
        network_bytes_sent INTEGER,
        network_bytes_received INTEGER,
        report_fk INTEGER,
        CONSTRAINT fk_report
            FOREIGN KEY (report_fk)
            REFERENCES report(report_pk)
    )
''')

cursor.execute('''
   CREATE TABLE IF NOT EXISTS process_metrics (
        process_metrics_pk INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        process_id INTEGER,
        process_name TEXT,
        process_command_line TEXT,
        process_cpu_percent INTEGER,
        process_memory_percent INTEGER,
        process_num_of_threads INTEGER,
        process_num_of_handles INTEGER,
        process_num_of_open_files INTEGER,
        process_read_count INTEGER,
        process_write_count INTEGER,
        report_fk INTEGER,
        CONSTRAINT fk_report
            FOREIGN KEY (report_fk)
            REFERENCES report(report_pk)
    )
''')

# Commit the changes and close the connection
connection.commit()
connection.close()
