import datetime
import logging
import subprocess
import time


class ExecuteTasks:

    def __init__(self,
                 script: object):
        self.script = script

    @staticmethod
    def execute_script(script, end_time):
        script_path = script['script_to_run']
        script_language = script['language']
        script_arguments = script['args']
        script_interval = script['interval']
        script_threads = script['threads']
        logging.info(f'Starting execution of {script_path} ({script_language}) with arguments: {script_arguments}')
        try:
            if script_language == 'python':
                command = f"Python, {script_path}, {script_arguments},{script_interval}, {script_threads}, {end_time}"
            elif script_language == 'powershell':
                command = f"PowerShell.exe, {script_path}, {script_arguments},{script_interval}, {script_threads}, {end_time}"
            else:
                logging.error(f'Unsupported scripting language: {script_language}')
                return
            subprocess.run(command)
            logging.info(f'{script_path} ({script_language}) executed successfully')
        except subprocess.CalledProcessError as e:
            logging.error(f'Error executing {script_path} ({script_language}): {e}')

        logging.info('----------------------------------------')
