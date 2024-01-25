import sqlite3
import pandas as pd
import plotly.express as px
# from get_report_fk import report_fk


# Placeholder until integrated with app
report_fk = 1

# Connect to the SQLite database
connection = sqlite3.connect('surefireinsights.db')
cursor = connection.cursor()

# Execute a query to fetch data
query = 'select timestamp, cpu_percent from system_metrics where report_fk = ?'
cursor.execute(query, str(report_fk))

# Fetch all the data and close the connection
data = cursor.fetchall()
connection.close()

# Convert the data to a Pandas DataFrame
df = pd.DataFrame(data, columns=['timestamp', 'cpu_percent'])

# Create an interactive scatter plot
fig = px.line(df, x='timestamp', y='cpu_percent', title='System Metrics - CPU Utilisation (%)', template="plotly_dark")

# Save the Plotly figure to an HTML file
fig.write_html('reports/system_metrics_cpu_percentage.html')
