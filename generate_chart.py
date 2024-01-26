import sqlite3
import pandas as pd
import plotly.express as px
import yaml
from get_report_fk import report_fk


# Load YAML configuration
with open('config/charts.yaml', 'r') as file:
    config = yaml.safe_load(file)

# Connect to the SQLite database
connection = sqlite3.connect('surefireinsights.db')

for chart_config in config.get('charts', []):
    chart_name = chart_config.get('chart_name')
    chart_query = chart_config.get('chart_query')
    chart_type = chart_config.get('chart_type')
    x_column_name = chart_config.get('x_column_name')
    y_column_name = chart_config.get('y_column_name')
    chart_title = chart_config.get('chart_title')
    template = chart_config.get('template')

    # Execute a query to fetch data
    cursor = connection.cursor()
    cursor.execute(chart_query, str(report_fk))
    data = cursor.fetchall()
    cursor.close()

    # Convert the data to a Pandas DataFrame
    df = pd.DataFrame(data, columns=[x_column_name, y_column_name])

    # Create an interactive scatter plot
    if chart_type == 'line':
        fig = px.line(df, x=x_column_name, y=y_column_name, title=chart_title, template=template)
    elif chart_type == 'bar':
        fig = px.bar(df, x=x_column_name, y=y_column_name, title=chart_title, template=template)
    elif chart_type == 'pie':
        fig = px.pie(df, names=x_column_name, values=y_column_name, title=chart_title, template=template)
    else:
        raise ValueError("Invalid chart type")

    # Save the Plotly figure to an HTML file
    fig.write_html(f'reports/{chart_name}.html')

# Close the database connection
connection.close()
