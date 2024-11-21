

class EmployeeManagementController:
    def __init__(self):
        from factories.model_factory import ModelFactory
        self.employee_service = ModelFactory.create_employee_service()

    def find_all(self):
        return self.employee_service.get_all_employees()

    def set_schedule_to_employee(self, schedule_id, employee_id):
        self.employee_service.set_schedule_to_employee(schedule_id, employee_id)

    def add_employee(self, last_name: str, first_name: str, middle_name: str, work_email: str, password: str):
        self.employee_service.add_employee(last_name, first_name, middle_name, work_email, password)

    def add_administrator(self, last_name: str, first_name: str, middle_name: str,
                          work_email: str, password: str, key_code: str):
        self.employee_service.add_administrator(last_name, first_name, middle_name,
                                                work_email, password, key_code)


