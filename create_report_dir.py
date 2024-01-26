import os

class GenerateReportDir:
    @staticmethod
    def create_report_dir(report_name):
        destination_directory = os.path.join(os.path.dirname(__file__), "reports", report_name)
        os.makedirs(destination_directory, exist_ok=True)