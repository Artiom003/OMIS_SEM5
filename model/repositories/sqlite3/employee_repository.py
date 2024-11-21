import sqlite3
import uuid
from model.instances.employee import Employee
from ..base_employee_repository import BaseEmployeeRepository


class EmployeeRepository(BaseEmployeeRepository):
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def get_cursor(self):
        return self.conn.cursor()

    def get_employee_by_work_email_and_password(self, work_email, password) -> Employee | None:
        self.cursor.execute('SELECT * FROM Employees WHERE work_email=? AND password=?',
                            (work_email, password, ))
        employee_tuple = self.cursor.fetchone()
        if employee_tuple:
            return Employee(*employee_tuple)
        else:
            return None

    def check_exists(self, work_email) -> int:

        self.cursor.execute('SELECT COUNT(*) FROM Employees WHERE work_email=?', (work_email,))
        count_result = self.cursor.fetchone()[0]
        return 1 if count_result > 0 else 0

    def get_all_employees(self) -> list[Employee]:
        self.cursor.execute('SELECT * FROM Employees')
        tuple_list: list[tuple] = self.cursor.fetchall()
        employees_list: list[Employee] = []
        for i in tuple_list:
            employees_list.append(Employee(*i))
        return employees_list

    def add_employee(self, surname, name, patronymic, work_email,
                     password, schedule_id, role='USER'):

        employee_id = str(uuid.uuid4())
        cursor = self.get_cursor()

        cursor.execute("""
            INSERT INTO Employees (id, password, name, surname, patronymic, work_email, role, schedule_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (employee_id, password, name, surname, patronymic, work_email, role, schedule_id))
        self.conn.commit()

    def set_schedule_to_employee(self, schedule_id, employee_id):
        cursor = self.get_cursor()
        cursor.execute("UPDATE Employees SET schedule_id=? WHERE id=?",
                       (schedule_id, employee_id))
        self.conn.commit()

    # для отладки
    def print(self):
        # Подключаемся к базе данных SQLite
        cursor = self.conn.cursor()

        # Запрос для получения всех таблиц в базе данных
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()

        # Перебираем все таблицы и выводим их содержимое
        for table_name in tables:
            table_name = table_name[0]  # Извлекаем имя таблицы из кортежа
            print(f"Содержимое таблицы '{table_name}':")

            # Запрашиваем данные из таблицы
            cursor.execute(f"SELECT * FROM {table_name};")
            rows = cursor.fetchall()

            # Если таблица не пуста, выводим строки
            if rows:
                for row in rows:
                    print(row)
            else:
                print("Таблица пуста.")

            print()  # Для разделения содержимого таблиц

