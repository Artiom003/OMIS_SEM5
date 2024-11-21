import uuid


class WorkSchedule:
    def __init__(self, id: uuid.UUID,
                 monday_start: str, monday_end: str,
                 tuesday_start: str, tuesday_end: str,
                 wednesday_start: str, wednesday_end: str,
                 thursday_start: str, thursday_end: str,
                 friday_start: str, friday_end: str,
                 saturday_start: str, saturday_end: str,
                 sunday_start: str, sunday_end: str):
        self._id = id
        self._monday_start = monday_start
        self._monday_end = monday_end
        self._tuesday_start = tuesday_start
        self._tuesday_end = tuesday_end
        self._wednesday_start = wednesday_start
        self._wednesday_end = wednesday_end
        self._thursday_start = thursday_start
        self._thursday_end = thursday_end
        self._friday_start = friday_start
        self._friday_end = friday_end
        self._saturday_start = saturday_start
        self._saturday_end = saturday_end
        self._sunday_start = sunday_start
        self._sunday_end = sunday_end

    @property
    def id(self) -> uuid.UUID:
        return self._id

    @property
    def monday_start(self) -> str:
        return self._monday_start

    @property
    def monday_end(self) -> str:
        return self._monday_end

    @property
    def tuesday_start(self) -> str:
        return self._tuesday_start

    @property
    def tuesday_end(self) -> str:
        return self._tuesday_end

    @property
    def wednesday_start(self) -> str:
        return self._wednesday_start

    @property
    def wednesday_end(self) -> str:
        return self._wednesday_end

    @property
    def thursday_start(self) -> str:
        return self._thursday_start

    @property
    def thursday_end(self) -> str:
        return self._thursday_end

    @property
    def friday_start(self) -> str:
        return self._friday_start

    @property
    def friday_end(self) -> str:
        return self._friday_end

    @property
    def saturday_start(self) -> str:
        return self._saturday_start

    @property
    def saturday_end(self) -> str:
        return self._saturday_end

    @property
    def sunday_start(self) -> str:
        return self._sunday_start

    @property
    def sunday_end(self) -> str:
        return self._sunday_end
