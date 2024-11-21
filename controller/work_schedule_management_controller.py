

class WorkScheduleManagementController:
    def __init__(self):
        from factories.model_factory import ModelFactory
        self.work_schedule_service = ModelFactory.create_work_schedule_service()

    def get_work_schedule_by_id(self, employee_id):
        return self.work_schedule_service.get_work_schedule_by_id(employee_id)

    def get_work_schedules(self):
        return self.work_schedule_service.get_work_schedules()

    def add_work_schedule(self, monday_start: str, monday_end: str,
                          tuesday_start: str, tuesday_end: str,
                          wednesday_start: str, wednesday_end: str,
                          thursday_start: str, thursday_end: str,
                          friday_start: str, friday_end: str,
                          saturday_start: str, saturday_end: str,
                          sunday_start: str, sunday_end: str):

        self.work_schedule_service.add_work_schedule(monday_start, monday_end,
                                                     tuesday_start, tuesday_end,
                                                     wednesday_start, wednesday_end,
                                                     thursday_start, thursday_end,
                                                     friday_start, friday_end,
                                                     saturday_start, saturday_end,
                                                     sunday_start, sunday_end)
