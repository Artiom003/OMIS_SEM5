import uuid
import sqlite3
from model.instances.notification import Notification
from ..base_notification_repository import BaseNotificationRepository


class NotificationRepository(BaseNotificationRepository):
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def get_cursor(self):
        return self.conn.cursor()

    def close_connection(self):
        self.conn.close()

    def add_notification(self, employee_id, date: str, time: str, seconds: int, text: str, status: int = 0):
        notification_id = str(uuid.uuid4())
        cursor = self.get_cursor()
        cursor.execute("""
          INSERT INTO Notifications (id, employee_id, date, time, seconds, text, status)
          VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (notification_id, str(employee_id), date, time, seconds, text, status))
        self.conn.commit()

    def get_notifications_by_employee_id(self, employee_id) -> list[Notification]:
        self.cursor.execute('SELECT * FROM Notifications WHERE employee_id=?',
                            (str(employee_id),))
        tuple_list: list[tuple] = self.cursor.fetchall()
        notifications_list: list[Notification] = []
        for i in tuple_list:
            notifications_list.append(Notification(*i))
        return notifications_list




