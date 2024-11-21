from view.center_window_helper import CenterWindowHelper
from view.base_view import BaseView
from factories.controller_factory import ControllerFactory
from factories.view_factory import ViewFactory
from model.exceptions.custom_exceptions import *

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


class AuthenticationView(BaseView):
    def __init__(self):

        super().__init__()
        self.controller = ControllerFactory.create_employee_auth_controller()

    def display_login_screen(self):
        # Уничтожаем все элементы предыдущего экрана
        for widget in self.winfo_children():
            widget.destroy()

        w, h = 300, 290
        self.geometry(f"{w}x{h}")

        CenterWindowHelper.center_window(self, w, h)
        self.attributes('-topmost', True)

        # Отключаем тулбар
        self.overrideredirect(True)

        style = ttk.Style()
        style.configure("Gray.TFrame", background="#D3D3D3")

        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        title_label = ttk.Label(main_frame, text="Авторизация", font=("Helvetica", 16))
        title_label.pack(pady=(0, 0))

        # Поле для ввода рабочего Email
        email_label = tk.Label(self, text="Рабочий Email")
        email_label.pack(pady=(0, 5))  # Отступ сверху

        self.work_email_entry = tk.Entry(self)
        self.work_email_entry.configure(justify='center')
        self.work_email_entry.pack(pady=0)


        # Заголовок для поля пароля
        password_label = tk.Label(self, text="Пароль")
        password_label.pack(pady=(5, 0))

        # Поле для ввода пароля и галочка для показа пароля
        password_frame = tk.Frame(self)  # Создаем рамку для сгруппирования
        password_frame.pack(pady=(5, 5))  # Отступ до рамки

        self.show_password_var = tk.BooleanVar()
        show_password_checkbutton = tk.Checkbutton(password_frame,
                                                   variable=self.show_password_var,
                                                   command=self.toggle_password_visibility)
        show_password_checkbutton.pack(side=tk.LEFT)  # Располагаем галочку слева

        self.password_entry = tk.Entry(password_frame, show="*")
        self.password_entry.configure(justify='center')
        self.password_entry.pack(side=tk.LEFT, padx=(0, 28))  # Поле ввода справа от галочки

        # Создаем кнопку "Войти в Систему"
        login_button = ttk.Button(self, text="Войти в Систему", command=self.login)
        login_button.pack(pady=7)

        # Кнопка "Регистрация Администратора"
        registration_button = ttk.Button(self, text="Регистрация Администратора",
                                        command=self.display_admin_registration_screen)
        registration_button.pack(pady=7)

        style = ttk.Style()
        style.configure("Red.TButton", background="red", foreground="red")
        style.map("Red.TButton", background=[("active", "red")])

        # Кнопка "Выход"
        exit_button = ttk.Button(self, text="Выход", command=self.on_exit, style="Red.TButton")
        exit_button.pack(pady=15)  # Отступ снизу

        self.mainloop()

    def toggle_password_visibility(self):
        if self.show_password_var.get():
            self.password_entry.config(show="")
        else:
            self.password_entry.config(show="*")

    def on_exit(self):
        exit(0)

    def login(self):

        # Логика входа в систему
        work_email = self.work_email_entry.get()
        password = self.password_entry.get()

        # Проверка на непустой ввод
        if not all([work_email, password]):
            tk.messagebox.showerror("Ошибка", "Заполните все поля!")
            return

        try:
            self.user: dict = self.controller.login(work_email, password)

        except UserDoesntExistsException:
            tk.messagebox.showerror("Ошибка", "Неверные данные!")
            return

        except Exception:
            tk.messagebox.showerror("Ошибка", "Неизвестная ошибка!")
            return
        selected_role = self.user["role"]

        self.add_break_time_to_employee()
        self.add_entered_notification()

        user = self.user

        if selected_role == "ADMINISTRATOR":

            tk.messagebox.showinfo("Успех", "Вы вошли в систему!")  # Окно успеха
            main_view_employee = ViewFactory.create_main_view()
            self.destroy()
            main_view_employee.display_main_screen_administrator(user)

        elif selected_role == "USER":
            tk.messagebox.showinfo("Успех", "Вы вошли в систему!")  # Окно успеха
            main_view_employee = ViewFactory.create_main_view()
            self.destroy()
            main_view_employee.display_main_screen_employee(user)

        else:
            tk.messagebox.showerror("Ошибка", "Ошибка с ролью пользователя!")
            return

    def add_entered_notification(self):
        controller = ControllerFactory.create_notifications_controller()
        return controller.add_entered_notification(self.user)

    def add_break_time_to_employee(self):
        controller = ControllerFactory.create_break_time_controller()
        return controller.add_break_time_to_employee(self.user['id'])

    def display_admin_registration_screen(self):

        # Очищаем все элементы предыдущего экрана
        for widget in self.winfo_children():
            widget.destroy()

        w, h = 280, 500
        self.geometry(f"{w}x{h}")
        CenterWindowHelper.center_window(self, w, h)

        # Отключаем тулбар
        self.overrideredirect(True)

        style = ttk.Style()
        style.configure("Gray.TFrame", background="#D3D3D3")

        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        title_label = ttk.Label(main_frame, text="Регистрация", font=("Helvetica", 16))
        title_label.pack(pady=(0, 0))

        title_label = ttk.Label(main_frame, text="администратора", font=("Helvetica", 16))
        title_label.pack(pady=(0, 0))

        # Поля для ввода данных
        surname_label = tk.Label(self, text="Фамилия")
        surname_label.pack(pady=(0, 5))
        self.surname_entry = tk.Entry(self)
        self.surname_entry.configure(justify='center')
        self.surname_entry.pack(pady=(0, 10))

        name_label = tk.Label(self, text="Имя")
        name_label.pack(pady=(0, 5))
        self.name_entry = tk.Entry(self)
        self.name_entry.configure(justify='center')
        self.name_entry.pack(pady=(0, 10))

        patronymic_label = tk.Label(self, text="Отчество")
        patronymic_label.pack(pady=(0, 5))
        self.patronymic_entry = tk.Entry(self)
        self.patronymic_entry.configure(justify='center')
        self.patronymic_entry.pack(pady=(0, 10))

        email_label = tk.Label(self, text="Рабочий Email")
        email_label.pack(pady=(0, 5))
        self.email_entry = tk.Entry(self)
        self.email_entry.configure(justify='center')
        self.email_entry.pack(pady=(0, 10))

        password_label = tk.Label(self, text="Пароль")
        password_label.pack(pady=(0, 5))
        self.password_entry = tk.Entry(self, show="")
        self.password_entry.configure(justify='center')
        self.password_entry.pack(pady=(0, 10))

        key_label = tk.Label(self, text="Ключ-код")
        key_label.pack(pady=(0, 5))
        self.key_entry = tk.Entry(self)
        self.key_entry.configure(justify='center')
        self.key_entry.pack(pady=(0, 10))

        # Кнопка "Зарегистрироваться"
        register_button = ttk.Button(self, text="Зарегистрироваться", command=self.register_admin)
        register_button.pack(pady=(15, 15))

        # Кнопка "Назад"
        back_button = ttk.Button(self, text="Назад", command=self.login_screen)
        back_button.pack(pady=(0, 15))

        self.mainloop()

    def login_screen(self):
        self.destroy()
        ViewFactory.create_authentication_view().display_login_screen()

    def register_admin(self):

        # Здесь происходит логика регистрации
        last_name = self.surname_entry.get()
        first_name = self.name_entry.get()
        middle_name = self.patronymic_entry.get()
        work_email = self.email_entry.get()
        password = self.password_entry.get()
        key_code = self.key_entry.get()

        # Проверка на непустой ввод
        if not all([last_name, first_name, middle_name, work_email, password, key_code]):
            tk.messagebox.showerror("Ошибка", "Заполните все поля!")
            return

        try:
            controller = ControllerFactory.create_employee_management_controller()
            controller.add_administrator(last_name, first_name, middle_name, work_email, password, key_code)
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
        except KeyCodeException:
            tk.messagebox.showerror("Ошибка", "Неверный код доступа!")
            return
        except UserExistsWithThisEmailException:
            tk.messagebox.showerror("Ошибка", "Данный администратор уже существует!")
            return
        except Exception:
            tk.messagebox.showerror("Ошибка", "Неизвестная ошибка!")
            return

        # После успешной регистрации:
        tk.messagebox.showinfo("Информация", "Администратор зарегистрирован!")
        self.login_screen()  # Переход на экран авторизации




