from ..base_work_schedule_service import BaseWorkScheduleService
from model.exceptions.custom_exceptions import WorkScheduleExistsException


class WorkScheduleService(BaseWorkScheduleService):
    def __init__(self):
        from factories.model_factory import ModelFactory

        self.work_schedule_validator = ModelFactory.create_work_schedule_validator()
        self.work_schedule_repository = ModelFactory.create_work_schedule_repository(self.FILE)

    def get_work_schedule_by_id(self, employee_id):

        work_schedule = self.work_schedule_repository.get_work_schedule_by_id(employee_id)

        if work_schedule:
            return work_schedule
        else:
            return None

    def get_work_schedules(self):

        work_schedules = self.work_schedule_repository.get_work_schedules()

        if work_schedules:
            return work_schedules
        else:
            return None

    def add_work_schedule(self, monday_start: str, monday_end: str,
                          tuesday_start: str, tuesday_end: str,
                          wednesday_start: str, wednesday_end: str,
                          thursday_start: str, thursday_end: str,
                          friday_start: str, friday_end: str,
                          saturday_start: str, saturday_end: str,
                          sunday_start: str, sunday_end: str):

        # нет смысла так как во view уже идёт обработка, причём хорошая
        # self.work_schedule_validator.validate_work_schedule(monday_start, monday_end,
        #                                                     tuesday_start, tuesday_end,
        #                                                     wednesday_start, wednesday_end,
        #                                                     thursday_start, thursday_end,
        #                                                     friday_start, friday_end,
        #                                                     saturday_start, saturday_end,
        #                                                     sunday_start, sunday_end)

        if not self.work_schedule_repository.check_exists(monday_start, monday_end,
                                                          tuesday_start, tuesday_end,
                                                          wednesday_start, wednesday_end,
                                                          thursday_start, thursday_end,
                                                          friday_start, friday_end,
                                                          saturday_start, saturday_end,
                                                          sunday_start, sunday_end):

            self.work_schedule_repository.add_work_schedule(monday_start, monday_end,
                                                            tuesday_start, tuesday_end,
                                                            wednesday_start, wednesday_end,
                                                            thursday_start, thursday_end,
                                                            friday_start, friday_end,
                                                            saturday_start, saturday_end,
                                                            sunday_start, sunday_end)
        else:
            raise WorkScheduleExistsException

