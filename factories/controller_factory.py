from controller.employee_auth_controller import EmployeeAuthController
from controller.employee_management_controller import EmployeeManagementController
from controller.notification_controller import NotificationController
from controller.work_schedule_management_controller import WorkScheduleManagementController
from controller.default_settings_controller import DefaultSettingsController
from controller.break_time_controller import BreakTimeController


class ControllerFactory:

    @staticmethod
    def create_employee_auth_controller():
        return EmployeeAuthController()

    @staticmethod
    def create_employee_management_controller():
        return EmployeeManagementController()

    @staticmethod
    def create_notifications_controller():
        return NotificationController()

    @staticmethod
    def create_work_schedule_management_controller():
        return WorkScheduleManagementController()

    @staticmethod
    def create_default_settings_controller():
        return DefaultSettingsController()

    @staticmethod
    def create_break_time_controller():
        return BreakTimeController()
