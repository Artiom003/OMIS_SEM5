from ..base_employee_service import BaseEmployeeService
from model.exceptions.custom_exceptions import UserExistsWithThisEmailException, UserDoesntExistsException


class EmployeeService(BaseEmployeeService):
    def __init__(self):
        from factories.model_factory import ModelFactory

        self.employee_validator = ModelFactory.create_employee_validator()
        self.employee_repository = ModelFactory.create_employee_repository(self.FILE)
        self.work_schedule_repository = ModelFactory.create_work_schedule_repository(self.FILE)

    def login(self, work_email, password):

        # проверка, есть ли в базе такой пользователь
        employee = self.employee_repository.get_employee_by_work_email_and_password(work_email, password)

        if employee:
            print("Найден в базе такой сотрудник")
            employee_dict = {"id": employee.id,
                             "name": employee.name,
                             "surname": employee.surname,
                             "patronymic": employee.patronymic,
                             "work_email": employee.work_email,
                             "role": employee.role,
                             "schedule_id": employee.schedule_id}
            return employee_dict
        else:
            raise UserDoesntExistsException

    def add_administrator(self, last_name: str, first_name: str, middle_name: str,
                          work_email: str, password: str, key_code):

        self.employee_validator.validate_employee(last_name, first_name, middle_name,
                                                  work_email, password, key_code)

        if not self.employee_repository.check_exists(work_email):

            schedule_id = self.work_schedule_repository.get_schedule_id("08:00", "18:00",
                                                                        "08:00", "18:00",
                                                                        "08:00", "18:00",
                                                                        "08:00", "18:00",
                                                                        "08:00", "18:00",
                                                                        "08:00", "18:00",
                                                                        "-", "-")

            self.employee_repository.add_employee(last_name, first_name, middle_name,
                                                  work_email, password, schedule_id, 'ADMINISTRATOR')
        else:
            raise UserExistsWithThisEmailException

    def add_employee(self, last_name: str, first_name: str, middle_name: str, work_email: str, password: str):
        # Проверка на уникальность в базе
        self.employee_validator.validate_employee(last_name, first_name, middle_name, work_email, password)

        if not self.employee_repository.check_exists(work_email):

            schedule_id = self.work_schedule_repository.get_schedule_id("08:00", "18:00",
                                                                        "08:00", "18:00",
                                                                        "08:00", "18:00",
                                                                        "08:00", "18:00",
                                                                        "08:00", "18:00",
                                                                        "08:00", "18:00",
                                                                        "-", "-")

            self.employee_repository.add_employee(last_name, first_name, middle_name,
                                                  work_email, password, schedule_id)
        else:
            raise UserExistsWithThisEmailException

    def set_schedule_to_employee(self, schedule_id, employee_id):
        self.employee_repository.set_schedule_to_employee(schedule_id, employee_id)

    def get_all_employees(self):
        employees = self.employee_repository.get_all_employees()
        result = []
        for employee in employees:
            employee_dict = {"id": employee.id,
                             "name": employee.name,
                             "surname": employee.surname,
                             "patronymic": employee.patronymic,
                             "work_email": employee.work_email,
                             "role": employee.role,
                             "schedule_id": employee.schedule_id}
            result.append(employee_dict)

        if result:
            return result
        else:
            return None

