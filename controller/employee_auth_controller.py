
class EmployeeAuthController:
    def __init__(self):
        from factories.model_factory import ModelFactory
        self.employee_service = ModelFactory.create_employee_service()

    def login(self, work_email, password):
        return self.employee_service.login(work_email, password)
