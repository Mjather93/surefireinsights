# Extract the report_pk for this report and store in a variable
import sqlite3


connection = sqlite3.connect('surefireinsights.db')
cursor = connection.cursor()
cursor.execute('''
    select max(report_pk) from report
''')
report_fk = cursor.fetchone()[0]
cursor.close()
connection.close()
