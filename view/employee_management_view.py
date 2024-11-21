from view.base_view import BaseView
from view.center_window_helper import CenterWindowHelper
from factories.controller_factory import ControllerFactory
from model.exceptions.custom_exceptions import *

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


class EmployeeManagementView(BaseView):

    def register_employee_screen(self, user):
        self.user = user
        w, h = 300, 280
        self.geometry(f"{w}x{h}")
        CenterWindowHelper.center_window(self, w, h)

        for widget in self.winfo_children():
            widget.destroy()

        self.overrideredirect(True)

        style = ttk.Style()
        style.configure("Gray.TFrame", background="#D3D3D3")

        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        title_label = ttk.Label(main_frame, text="Регистрация cотрудника", font=("Helvetica", 16))
        title_label.pack(pady=(0, 10))

        labels_entries = [
            ("Фамилия:", "last_name"),
            ("Имя:", "first_name"),
            ("Отчество:", "middle_name"),
            ("Рабочий Email:", "work_email"),
            ("Пароль:", "password"),
        ]

        self.entries = {}

        for label_text, entry_name in labels_entries:
            frame = ttk.Frame(main_frame, style="Gray.TFrame", padding="5")
            frame.pack(fill=tk.X, pady=(5, 0))

            centered_frame = ttk.Frame(frame)
            centered_frame.pack(side=tk.LEFT, expand=True)

            label = ttk.Label(centered_frame, text=label_text, font=("Helvetica", 12))
            label.pack(side=tk.LEFT)

            entry = ttk.Entry(frame, width=30)
            entry.config(justify='center')
            entry.pack(side=tk.LEFT, padx=(5, 0))
            self.entries[entry_name] = entry

        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=(10, 0))

        create_button = ttk.Button(button_frame, text="Зарегистрировать Cотрудника", command=self.create_user)
        create_button.pack(side=tk.LEFT, padx=(0, 10))

        back_button = ttk.Button(button_frame, text="Назад", command=self.display_main_screen)
        back_button.pack(side=tk.LEFT)

    def create_user(self):
        employee_data = {}
        for key, entry in self.entries.items():
            employee_data[key] = entry.get()

        # Проверка на пустые поля
        if any(not value for value in employee_data.values()):
            messagebox.showerror("Ошибка", "Все поля должны быть заполнены!")
            return

        # Извлечение данных в отдельные переменные
        last_name = employee_data.get("last_name")
        first_name = employee_data.get("first_name")
        middle_name = employee_data.get("middle_name")
        work_email = employee_data.get("work_email")
        password = employee_data.get("password")

        try:
            # Здесь реализуйте логику создания пользователя, используя извлеченные данные
            controller = ControllerFactory.create_employee_management_controller()
            controller.add_employee(last_name, first_name, middle_name, work_email, password)

        except LastNameException:
            tk.messagebox.showerror("Ошибка", "Ошибка в фамилии!")
            return
        except FirstNameException:
            tk.messagebox.showerror("Ошибка", "Ошибка в имени!")
            return
        except MiddleNameException:
            tk.messagebox.showerror("Ошибка", "Ошибка в отчестве!")
            return
        except WorkEmailException:
            tk.messagebox.showerror("Ошибка", "Неверный формат email!")
            return
        except PasswordException:
            tk.messagebox.showerror("Ошибка", "Пароль не должен содержать пробелы!")
            return
        except UserExistsWithThisEmailException:
            tk.messagebox.showerror("Ошибка", "Данный сотрудник уже существует!")
            return
        except Exception:
            tk.messagebox.showerror("Ошибка", "Неизвестная ошибка!")
            return

        messagebox.showinfo("Успех", "Пользователь успешно зарегистрирован!")
        self.display_main_screen()

    def display_main_screen(self):
        from factories.view_factory import ViewFactory
        self.destroy()
        main_view_employee = ViewFactory.create_main_view()
        main_view_employee.display_main_screen_administrator(self.user)

