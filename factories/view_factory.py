from view.main_view import MainView
from view.employee_management_view import EmployeeManagementView
from view.work_schedule_management_view import WorkScheduleManagementView


class ViewFactory:

    @staticmethod
    def create_authentication_view():
        from view.authentication_view import AuthenticationView
        return AuthenticationView()

    @staticmethod
    def create_main_view():
        return MainView()

    @staticmethod
    def create_employee_management_view():
        return EmployeeManagementView()

    @staticmethod
    def work_schedule_management_view():
        return WorkScheduleManagementView()



