import shutil
import os
import sqlite3


class GenerateReport:
    @staticmethod
    def create_report_files(report_name):
        # Source directory and file paths
        source_directory = os.path.join(os.path.dirname(__file__), "reports", "template")
        source_file_path = os.path.join(source_directory, "index-template.html")

        # Destination directory and file paths
        destination_directory = os.path.join(os.path.dirname(__file__), "reports", report_name)
        destination_file_path = os.path.join(destination_directory, f"{report_name}.html")

        # Copy the HTML file to the parent directory with the new name
        os.makedirs(destination_directory, exist_ok=True)
        shutil.copy(source_file_path, destination_file_path)

        # Copy the 'static' directory and its contents
        static_source_directory = os.path.join(source_directory, "static")
        static_destination_directory = os.path.join(destination_directory, "static")

        shutil.copytree(static_source_directory, static_destination_directory, dirs_exist_ok=True)

    @staticmethod
    def update_report(report_name):
        # Report file to open
        report_directory = os.path.join(os.path.dirname(__file__), "reports", report_name)
        html_file = os.path.join(report_directory, f"{report_name}.html")

        # SQL to get values we don't already have
        connection = sqlite3.connect('surefireinsights.db')
        cursor = connection.cursor()
        cursor.execute('''
            select monitoring_start_time, monitoring_end_time from report
            where report_pk = (select max(report_pk) from report)
        ''')
        results = cursor.fetchone()
        monitoring_start_time = results[0]
        monitoring_end_time = results[1]
        cursor.close()
        connection.close()

        replacements = {
            'REPLACENAME': report_name,
            'REPLACESTARTTIME': monitoring_start_time,
            'REPLACEENDTIME': monitoring_end_time
        }

        try:
            # Read the content of the input HTML file
            with open(html_file, 'r', encoding='utf-8') as file:
                html_content = file.read()

            # Perform string replacements
            for old_string, new_value in replacements.items():
                html_content = html_content.replace(old_string, str(new_value))

            # Write the modified content to the output HTML file
            with open(html_file, 'w', encoding='utf-8') as file:
                file.write(html_content)

            print(f"File '{html_file}' has been successfully updated.")
        except Exception as e:
            print(f"An error occurred: {e}")

        # Add in system metrics links
        # Find all files in the directory containing '_system_metrics_' in the file name
        matching_files = [file for file in os.listdir(report_directory) if '_system_metrics_' in file]

        # Generate a list of HTML link elements
        links_list = [f'<a href="{os.path.join(report_directory, file)}" target="_blank">{file}</a><br>' for file in
                      matching_files]

        # Read the content of the existing HTML file
        with open(html_file, 'r', encoding='utf-8') as existing_file:
            html_content = existing_file.read()

        # Join the list of links into a single string
        links_content = '\n'.join(links_list)

        # Find and replace the placeholder text with the generated links
        html_content = html_content.replace('ADDSYSTEMMETRICSLINKS', links_content)

        # Write the modified content back to the same HTML file
        with open(html_file, 'w', encoding='utf-8') as modified_file:
            modified_file.write(html_content)
