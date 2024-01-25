import sqlite3
from datetime import datetime
from get_report_fk import report_fk


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
''', (monitoring_end_time, report_fk))
connection.commit()
cursor.close()
connection.close()
