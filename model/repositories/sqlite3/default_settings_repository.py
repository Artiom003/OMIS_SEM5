import sqlite3
from ..base_default_settings_repository import BaseDefaultSettingsRepository


class DefaultSettingsRepository(BaseDefaultSettingsRepository):
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def get_cursor(self):
        return self.conn.cursor()

    def create_tables(self):
        self.cursor.execute("""
                            CREATE TABLE IF NOT EXISTS Employees (
                                id TEXT PRIMARY KEY,
                                password TEXT, 
                                name TEXT,
                                surname TEXT,
                                patronymic TEXT,
                                work_email TEXT,
                                role TEXT,
                                schedule_id,
                                FOREIGN KEY (schedule_id) REFERENCES Schedules(id)                     
                            )""")

        self.cursor.execute("""
                            CREATE TABLE IF NOT EXISTS Schedules (
                                id TEXT PRIMARY KEY,
            
                                monday_start TEXT,
                                monday_end TEXT,
            
                                tuesday_start TEXT,
                                tuesday_end TEXT,
            
                                wednesday_start TEXT,
                                wednesday_end TEXT,
            
                                thursday_start TEXT,
                                thursday_end TEXT,
            
                                friday_start TEXT,
                                friday_end TEXT,
            
                                saturday_start TEXT,
                                saturday_end TEXT,
            
                                sunday_start TEXT,
                                sunday_end TEXT
                            )""")

        self.cursor.execute("""
                            CREATE TABLE IF NOT EXISTS Notifications (
                              id TEXT PRIMARY KEY,
                              employee_id TEXT,
                              date TEXT,
                              time TEXT,
                              seconds INTEGER,
                              text TEXT,
                              status INTEGER,
                              FOREIGN KEY (employee_id) REFERENCES Employees(id)
                            )""")

        self.cursor.execute("""
                            CREATE TABLE IF NOT EXISTS BreakTimes (
                                id TEXT PRIMARY KEY,
                                employee_id TEXT,
                                date TEXT,
                                break_time_min INTEGER,
                                break_time_sec INTEGER,
                                penalty_time_min INTEGER,
                                penalty_time_sec INTEGER,
                                FOREIGN KEY (employee_id) REFERENCES Employees(id)
                            )""")

        self.conn.commit()
