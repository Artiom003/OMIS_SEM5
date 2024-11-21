import datetime


class WorkingHours:
    def __init__(self, start_hour: datetime.time, end_hour: datetime.time):
        self._start_hour = start_hour
        self._end_hour = end_hour

    @property
    def start_hour(self) -> datetime.time:
        return self._start_hour

    @property
    def end_hour(self) -> datetime.time:
        return self._end_hour

    @start_hour.setter
    def start_hour(self, value: datetime.time):
        self._start_hour = value

    @end_hour.setter
    def end_hour(self, value: datetime.time):
        self._end_hour = value
