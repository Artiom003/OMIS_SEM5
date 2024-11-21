import uuid


class Notification:
    def __init__(self, id: uuid.UUID,  employee_id: uuid.UUID, date: str,
                 time: str, seconds: str, text: str, status: int):
        self._id = id,
        self._employee_id = employee_id
        self._date = date
        self._time = time
        self._seconds = seconds
        self._text = text
        self._status = status

    @property
    def id(self) -> uuid.UUID:
        return self._id

    @property
    def employee_id(self) -> uuid.UUID:
        return self._employee_id

    @property
    def date(self) -> str:
        return self._date

    @property
    def time(self) -> str:
        return self._time

    @property
    def seconds(self) -> str:
        return self._seconds

    @property
    def text(self) -> str:
        return self._text

    @property
    def status(self) -> int:
        return self._status

    @id.setter
    def id(self, value: uuid.UUID):
        self._id = value

    @employee_id.setter
    def employee_id(self, value: uuid.UUID):
        self._employee_id = value

    @date.setter
    def date(self, value: str):
        self._date = value

    @time.setter
    def time(self, value: str):
        self._time = value

    @seconds.setter
    def seconds(self, value: str):
        self._seconds = value

    @text.setter
    def text(self, value: str):
        self._text = value

    @status.setter
    def status(self, value: str):
        self._status = value

