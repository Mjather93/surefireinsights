from datetime import datetime
import sqlite3
import logging_config

# Import logging configuration
logging_config.logging_config()


class ConfigureMonitoring:
    @staticmethod
    def save_config(report_name, monitoring_duration):
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
