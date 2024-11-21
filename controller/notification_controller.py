

class NotificationController:
    def __init__(self):
        from factories.model_factory import ModelFactory
        self.notification_service = ModelFactory.create_notification_service()

    def get_notifications_today_by_employee_id(self, employee_id):
        return self.notification_service.get_notifications_today_by_employee_id(employee_id)

    def add_entered_notification(self, employee):
        return self.notification_service.add_entered_notification(employee)

    def add_exit_notification(self, employee):
        return self.notification_service.add_exit_notification(employee)
