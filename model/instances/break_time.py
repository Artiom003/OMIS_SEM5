import uuid


class BreakTime:
    def __init__(self, id: uuid.UUID, employee_id: uuid.UUID, date: str,
                 break_time_min: int, break_time_sec: int, penalty_time_min: int, penalty_time_sec: int):
        self._id = id
        self._employee_id = employee_id
        self._date = date
        self._break_time_min = break_time_min
        self._break_time_sec = break_time_sec
        self._penalty_time_min = penalty_time_min
        self._penalty_time_sec = penalty_time_sec

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
    def break_time_min(self) -> int:
        return self._break_time_min

    @property
    def penalty_time_min(self) -> int:
        return self._penalty_time_min

    @property
    def break_time_sec(self) -> int:
        return self._break_time_sec

    @property
    def penalty_time_sec(self) -> int:
        return self._penalty_time_sec

    @id.setter
    def id(self, value: uuid.UUID):
        self._id = value

    @employee_id.setter
    def employee_id(self, value: uuid.UUID):
        self._employee_id = value

    @date.setter
    def date(self, value: str):
        self._date = value

    @break_time_min.setter
    def break_time_min(self, value: int):
        self._break_time_min = value

    @penalty_time_min.setter
    def penalty_time_min(self, value: int):
        self._penalty_time_min = value

    @break_time_sec.setter
    def break_time_sec(self, value: int):
        self._break_time_sec = value

    @penalty_time_sec.setter
    def penalty_time_sec(self, value: int):
        self._penalty_time_sec = value

