
class BreakTimeController:
    def __init__(self):
        from factories.model_factory import ModelFactory
        self.break_time_service = ModelFactory.create_break_time_service()

    def set_break_time_and_penalty_time_to_employee_id_and_date(self, employee_id,
                                                                break_time_min, break_time_sec,
                                                                penalty_time_min, penalty_time_sec):
        self.break_time_service.set_break_time_and_penalty_time_to_employee_id_and_date(employee_id,
                                                                                        break_time_min, break_time_sec,
                                                                                        penalty_time_min,
                                                                                        penalty_time_sec)

    def get_break_time_by_employee_id(self, employee_id):
        return self.break_time_service.get_break_time_by_employee_id(employee_id)

    def add_break_time_to_employee(self, employee_id):
        self.break_time_service.add_break_time_to_employee(employee_id)
