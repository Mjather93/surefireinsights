import logging
import sqlite3
import logging_config


# Import logging configuration
logging_config.logging_config()
print("connecting to db")
# Connect to SQLite database (or create if it doesn't exist)
connection = sqlite3.connect('surefireinsights.db')

# Create a cursor object to execute SQL queries
cursor = connection.cursor()
try:
    with open('install/install.sql', 'r') as sql_file:
        sql_script = sql_file.read()
        logging.debug(f"SQL Script being run: \n{sql_script}")
        cursor.executescript(sql_script)
        connection.commit()

except Exception as e:
    # Handle exceptions if there's an error in the SQL file
    logging.error(f"Error executing SQL file: {e}")

finally:
    cursor.close()
    connection.close()
