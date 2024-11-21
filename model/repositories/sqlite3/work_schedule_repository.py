import sqlite3
import uuid
from model.instances.work_schedule import WorkSchedule
from ..base_work_schedule_repository import BaseWorkScheduleRepository


class WorkScheduleRepository(BaseWorkScheduleRepository):
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def get_cursor(self):
        return self.conn.cursor()

    def close_connection(self):
        self.conn.close()

    def get_work_schedules(self) -> list[WorkSchedule]:
        self.cursor.execute('SELECT * FROM Schedules')
        tuple_list: list[tuple] = self.cursor.fetchall()
        work_schedules_list: list[WorkSchedule] = []
        for i in tuple_list:
            work_schedules_list.append(WorkSchedule(*i))
        return work_schedules_list

    def check_exists(self, monday_start: str, monday_end: str,
                     tuesday_start: str, tuesday_end: str,
                     wednesday_start: str, wednesday_end: str,
                     thursday_start: str, thursday_end: str,
                     friday_start: str, friday_end: str,
                     saturday_start: str, saturday_end: str,
                     sunday_start: str, sunday_end: str):
        cursor = self.get_cursor()  # Получаем курсор для выполнения запросов к базе данных

        # SQL-запрос для проверки существования расписания
        query = """
            SELECT COUNT(*) FROM Schedules
            WHERE monday_start = ? AND monday_end = ?
              AND tuesday_start = ? AND tuesday_end = ?
              AND wednesday_start = ? AND wednesday_end = ?
              AND thursday_start = ? AND thursday_end = ?
              AND friday_start = ? AND friday_end = ?
              AND saturday_start = ? AND saturday_end = ?
              AND sunday_start = ? AND sunday_end = ?
        """

        cursor.execute(query, (monday_start, monday_end,
                               tuesday_start, tuesday_end,
                               wednesday_start, wednesday_end,
                               thursday_start, thursday_end,
                               friday_start, friday_end,
                               saturday_start, saturday_end,
                               sunday_start, sunday_end))

        exists = cursor.fetchone()[0]  # Получаем количество найденных расписаний

        return exists > 0

    def add_work_schedule(self, monday_start: str, monday_end: str,
                          tuesday_start: str, tuesday_end: str,
                          wednesday_start: str, wednesday_end: str,
                          thursday_start: str, thursday_end: str,
                          friday_start: str, friday_end: str,
                          saturday_start: str, saturday_end: str,
                          sunday_start: str, sunday_end: str):
        work_schedule_id = str(uuid.uuid4())  # Генерация нового уникального идентификатора для расписания работы

        cursor = self.get_cursor()  # Получаем курсор для выполнения запросов к базе данных

        # Выполняем SQL-запрос для вставки нового расписания работы в таблицу
        cursor.execute("""
            INSERT INTO Schedules (id, monday_start, monday_end,
                                       tuesday_start, tuesday_end,
                                       wednesday_start, wednesday_end,
                                       thursday_start, thursday_end,
                                       friday_start, friday_end,
                                       saturday_start, saturday_end,
                                       sunday_start, sunday_end)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (work_schedule_id, monday_start, monday_end,
              tuesday_start, tuesday_end,
              wednesday_start, wednesday_end,
              thursday_start, thursday_end,
              friday_start, friday_end,
              saturday_start, saturday_end,
              sunday_start, sunday_end))

        self.conn.commit()

    def get_work_schedule_by_id(self, id) -> WorkSchedule | None:
        self.cursor.execute('SELECT * FROM Schedules WHERE id=?',
                            (id, ))
        work_schedule_tuple = self.cursor.fetchone()
        if work_schedule_tuple:
            return WorkSchedule(*work_schedule_tuple)
        else:
            return None

    def get_schedule_id(self, monday_start: str, monday_end: str,
                        tuesday_start: str, tuesday_end: str,
                        wednesday_start: str, wednesday_end: str,
                        thursday_start: str, thursday_end: str,
                        friday_start: str, friday_end: str,
                        saturday_start: str, saturday_end: str,
                        sunday_start: str, sunday_end: str) -> uuid:
        query = """
          SELECT id 
          FROM Schedules 
          WHERE monday_start = ? AND monday_end = ? AND 
             tuesday_start = ? AND tuesday_end = ? AND
             wednesday_start = ? AND wednesday_end = ? AND
             thursday_start = ? AND thursday_end = ? AND
             friday_start = ? AND friday_end = ? AND
             saturday_start = ? AND saturday_end = ? AND
             sunday_start = ? AND sunday_end = ?;
        """
        self.cursor.execute(query, (monday_start, monday_end, tuesday_start, tuesday_end,
                                    wednesday_start, wednesday_end, thursday_start, thursday_end,
                                    friday_start, friday_end, saturday_start, saturday_end,
                                    sunday_start, sunday_end))

        result = self.cursor.fetchall()
        if len(result) == 1:
            return result[0][0]
        else:
            return None

    def update_work_schedule_by_id(self, id,
                                   monday_start: str, monday_end: str,
                                   tuesday_start: str, tuesday_end: str,
                                   wednesday_start: str, wednesday_end: str,
                                   thursday_start: str, thursday_end: str,
                                   friday_start: str, friday_end: str,
                                   saturday_start: str, saturday_end: str,
                                   sunday_start: str, sunday_end: str):
        cursor = self.get_cursor()  # Получаем курсор для выполнения запросов к базе данных

        # Выполняем SQL-запрос для обновления расписания работы по идентификатору
        cursor.execute("""
            UPDATE Schedules 
            SET monday_start = ?, monday_end = ?,
                tuesday_start = ?, tuesday_end = ?,
                wednesday_start = ?, wednesday_end = ?,
                thursday_start = ?, thursday_end = ?,
                friday_start = ?, friday_end = ?,
                saturday_start = ?, saturday_end = ?,
                sunday_start = ?, sunday_end = ?
            WHERE id = ?
        """, (monday_start, monday_end,
              tuesday_start, tuesday_end,
              wednesday_start, wednesday_end,
              thursday_start, thursday_end,
              friday_start, friday_end,
              saturday_start, saturday_end,
              sunday_start, sunday_end,
              id))  # Передача id в конце параметров

        self.conn.commit()  # Сохраняем изменения в базе данных
