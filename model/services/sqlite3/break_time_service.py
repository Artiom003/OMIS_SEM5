from ..base_break_time_service import BaseBreakTimeService


class BreakTimeService(BaseBreakTimeService):
    def __init__(self):
        from factories.model_factory import ModelFactory

        self.employee_repository = ModelFactory.create_employee_repository(self.FILE)
        self.break_time_repository = ModelFactory.create_break_time_repository(self.FILE)

    def set_break_time_and_penalty_time_to_employee_id_and_date(self, employee_id,
                                                                break_time_min, break_time_sec,
                                                                penalty_time_min, penalty_time_sec):
        import datetime

        current_time = datetime.datetime.now()
        current_date = current_time.strftime('%d.%m.%Y')
        self.break_time_repository.set_break_time_and_penalty_time_to_employee_id_and_date(employee_id, current_date,
                                                                                           break_time_min,
                                                                                           break_time_sec,
                                                                                           penalty_time_min,
                                                                                           penalty_time_sec)

    def get_break_time_by_employee_id(self, employee_id):
        import datetime

        current_time = datetime.datetime.now()
        current_date = current_time.strftime('%d.%m.%Y')

        return self.break_time_repository.get_break_time_by_employee_id_and_date(employee_id, current_date)

    def add_break_time_to_employee(self, employee_id):
        import datetime

        current_time = datetime.datetime.now()
        current_date = current_time.strftime('%d.%m.%Y')
        if not self.break_time_repository.check_break_time(employee_id, current_date):
            self.break_time_repository.add_break_time(employee_id, current_date, 0, 10, 0, 0)



