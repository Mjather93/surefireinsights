import datetime


class ExecuteTasks:

    def __init__(self,
                 duration: int,
                 interval: int,
                 start_time):
        self.end_time = None
        self.start_time = start_time
        self.duration = duration
        self.interval = interval

    def calculate_end_time(self):
        try:
            start_time_formatted = datetime.datetime(self.start_time, '%d-%m-%Y %H:%M:%S.%f')[:-3]
            time_delta = datetime.timedelta(seconds=self.duration)
            self.start_time = start_time_formatted
            self.end_time = start_time_formatted + time_delta
            return self.end_time
        except Exception as e:
            return f'Exception raised: {e}'

    def work_to_do(self):


