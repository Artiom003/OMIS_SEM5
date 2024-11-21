import uuid
import sqlite3
from model.instances.break_time import BreakTime
from ..base_break_time_repository import BaseBreakTimeRepository


class BreakTimeRepository(BaseBreakTimeRepository):
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def get_cursor(self):
        return self.conn.cursor()

    def close_connection(self):
        self.conn.close()

    def check_break_time(self, employee_id, date) -> int:
        cursor = self.get_cursor()
        cursor.execute('SELECT COUNT(*) FROM BreakTimes WHERE employee_id=? AND date=?',
                       (str(employee_id), str(date)))
        count_result = cursor.fetchone()[0]
        return 1 if count_result > 0 else 0

    def add_break_time(self, employee_id, date: str, break_time_min: int, break_time_sec: int,
                       penalty_time_min: int,  penalty_time_sec: int):
        id = str(uuid.uuid4())
        cursor = self.get_cursor()
        cursor.execute("""
          INSERT INTO BreakTimes (id, employee_id, date, break_time_min, break_time_sec,
                                  penalty_time_min, penalty_time_sec)
          VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (id, str(employee_id), date, break_time_min,
              break_time_sec, penalty_time_min, penalty_time_sec))
        self.conn.commit()
        print("Добавлено время перерыва")

    def get_break_time_by_employee_id_and_date(self, employee_id, date) -> BreakTime | None:
        self.cursor.execute('SELECT * FROM BreakTimes WHERE employee_id=? and date=?',
                            (str(employee_id), str(date),))
        break_time_tuple = self.cursor.fetchone()
        if break_time_tuple:
            return BreakTime(*break_time_tuple)
        else:
            return None

    def set_break_time_and_penalty_time_to_employee_id_and_date(self, employee_id, date,
                                                                break_time_min, break_time_sec,
                                                                penalty_time_min, penalty_time_sec):
        cursor = self.get_cursor()
        cursor.execute("""
                    UPDATE BreakTimes
                    SET break_time_min = ?, break_time_sec = ?, penalty_time_min = ?, penalty_time_sec = ?
                    WHERE employee_id = ? AND date = ?
                    """, (break_time_min, break_time_sec, penalty_time_min, penalty_time_sec,
                          employee_id, date))

        self.conn.commit()  # Сохраняем изменения в базе данных



