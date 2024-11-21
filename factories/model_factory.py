from model.repositories.sqlite3.employee_repository import EmployeeRepository
from model.repositories.sqlite3.work_schedule_repository import WorkScheduleRepository
from model.repositories.sqlite3.notification_repository import NotificationRepository
from model.repositories.sqlite3.default_settings_repository import DefaultSettingsRepository
from model.repositories.sqlite3.break_time_repository import BreakTimeRepository

from model.services.sqlite3.employee_service import EmployeeService
from model.services.sqlite3.work_schedule_service import WorkScheduleService
from model.services.sqlite3.notification_service import NotificationService
from model.services.sqlite3.default_settings_service import DefaultSettingsService
from model.services.sqlite3.break_time_service import BreakTimeService

from model.validators.employee_validator import EmployeeValidator
from model.validators.work_schedule_validator import WorkScheduleValidator


class ModelFactory:

    @staticmethod
    def create_employee_repository(db_name):
        return EmployeeRepository(db_name)

    @staticmethod
    def create_work_schedule_repository(db_name):
        return WorkScheduleRepository(db_name)

    @staticmethod
    def create_notification_repository(db_name):
        return NotificationRepository(db_name)

    @staticmethod
    def create_default_settings_repository(db_name):
        return DefaultSettingsRepository(db_name)

    @staticmethod
    def create_break_time_repository(db_name):
        return BreakTimeRepository(db_name)

    @staticmethod
    def create_employee_service():
        return EmployeeService()

    @staticmethod
    def create_work_schedule_service():
        return WorkScheduleService()

    @staticmethod
    def create_notification_service():
        return NotificationService()

    @staticmethod
    def create_default_settings_service():
        return DefaultSettingsService()

    @staticmethod
    def create_break_time_service():
        return BreakTimeService()

    @staticmethod
    def create_employee_validator():
        return EmployeeValidator()

    @staticmethod
    def create_work_schedule_validator():
        return WorkScheduleValidator()
