from factories.view_factory import ViewFactory
from factories.controller_factory import ControllerFactory
import sqlite3
from tkinter import messagebox


class Application:

    @staticmethod
    def run():
        try:
            ControllerFactory.create_default_settings_controller().set_default_settings()
            ViewFactory.create_authentication_view().display_login_screen()
        except sqlite3.OperationalError:
            messagebox.showerror("Ошибка", "Ошибка соединения с базой данных!")
            return



