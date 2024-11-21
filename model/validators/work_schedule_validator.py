import re
from model.exceptions.custom_exceptions import WorkScheduleException


class WorkScheduleValidator:
    def validate_time_format(self, time_str):
        """Проверяет формат времени HH:MM-HH:MM."""
        pattern = re.compile(r'^(?:[01]\d|2[0-3]):[0-5]\d-(?:[01]\d|2[0-3]):[0-5]\d$')
        return bool(pattern.match(time_str))

    def validate_work_schedule(self, monday_start, monday_end,
                               tuesday_start, tuesday_end,
                               wednesday_start, wednesday_end,
                               thursday_start, thursday_end,
                               friday_start, friday_end,
                               saturday_start, saturday_end,
                               sunday_start, sunday_end):
        """Валидирует график работы, используя предоставленную структуру аргументов."""

        weekly_schedule = [
            (monday_start, monday_end),
            (tuesday_start, tuesday_end),
            (wednesday_start, wednesday_end),
            (thursday_start, thursday_end),
            (friday_start, friday_end),
            (saturday_start, saturday_end),
            (sunday_start, sunday_end)
        ]

        for i, (start, end) in enumerate(weekly_schedule):
            if start != "-" and end != "-":
                if not self.validate_time_format(start + "-" + end):
                    raise WorkScheduleException
                try:
                    start_h, start_m = map(int, start.split(':'))
                    end_h, end_m = map(int, end.split(':'))
                    if (end_h, end_m) <= (start_h, start_m):
                        raise WorkScheduleException(
                            f"Время окончания работы должно быть позже времени начала для дня {i + 1}")
                except ValueError:
                    raise WorkScheduleException(f"Неверный формат времени для дня {i + 1}")
