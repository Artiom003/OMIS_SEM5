from view.base_view import BaseView
from view.center_window_helper import CenterWindowHelper
from factories.controller_factory import ControllerFactory

import tkinter as tk
from tkinter import messagebox, ttk


class MainView(BaseView):

    def display_main_screen_employee(self, user):
        self.user = user
        w, h = 905, 430
        self.geometry(f"{w}x{h}")
        CenterWindowHelper.center_window(self, w, h)
        self.attributes('-topmost', True)

        # Отключаем тулбар
        self.overrideredirect(True)

        # Уничтожаем все элементы предыдущего экрана
        for widget in self.winfo_children():
            widget.destroy()

        # Уменьшаем отступы в main_frame
        self.main_frame = ttk.Frame(self, padding="0")  # Убираем или уменьшаем отступы
        self.main_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        notifications = self.get_notifications_today()
        schedule = self.get_work_schedule_by_id()

        self.display_schedule(schedule)

        self.left_frame = ttk.Frame(self)  # Уменьшаем отступы
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, pady=(0, 1), padx=(5, 0))

        self.create_notifications_area(notifications)

        self.timer_running = False
        self.finish_break_button = None
        self.late_timer_running = False

        self.break_time = self.get_break_time_by_employee_id()

        # Уменьшаем отступы в правом и левом фреймах
        self.right_frame = ttk.Frame(self)  # Уменьшаем отступы
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(0, 0))

        # Создаем кнопки
        self.create_user_buttons()

        # Создаем рамку для всего блока информации о пользователе и таймера
        right_outer_frame = tk.Frame(self.right_frame, bd=2, relief=tk.RIDGE)
        right_outer_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True, padx=10, pady=(10, 10))
        # Заголовок для правой части (имя, фамилия, email)

        right_text_outer_frame = tk.Frame(self.right_frame)
        right_text_outer_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=(6, 0))

        user_info_label = tk.Label(right_text_outer_frame,
                                   text=f"{self.user['surname']} "
                                        f"{self.user['name']} "
                                        f"{self.user['patronymic']}"
                                        + '\n' + self.user["work_email"],
                                   font=("Helvetica", 16, 'bold'))

        user_info_label.pack(anchor='n', pady=(0, 0), side=tk.TOP)  # Уменьшаем pady для меньших отступов

        # Фрейм для информации о пользователе
        self.user_info_container = tk.Frame(right_outer_frame)
        self.user_info_container.pack(fill=tk.BOTH, expand=True, padx=0, pady=2, side=tk.TOP)

        # Инициализация таймера
        self.break_time_minutes = self.break_time.break_time_min  # Получаем минуты из объекта BreakTime
        self.break_time_seconds = self.break_time_minutes * 60  # Переводим в секунды
        self.break_time_seconds = self.break_time_seconds + self.break_time.break_time_sec

        self.late_minutes = self.break_time.penalty_time_min
        self.late_seconds = self.late_minutes * 60
        self.late_seconds = self.late_seconds + self.break_time.penalty_time_sec

        self.finish_break_button = ttk.Button(right_outer_frame, text="Закончить Перерыв",
                                              command=self.finish_break)
        self.finish_break_button.pack(side=tk.BOTTOM, pady=(0, 20))

        # Изначально кнопка "Закончить Перерыв" неактивна
        self.finish_break_button.config(state=tk.DISABLED)

        self.create_timer()  # Создадим таймер при инициализации

    def display_main_screen_administrator(self, user):
        self.user = user
        w, h = 905, 430
        self.geometry(f"{w}x{h}")
        CenterWindowHelper.center_window(self, w, h)
        self.attributes('-topmost', True)

        # Отключаем тулбар
        self.overrideredirect(True)

        # Уничтожаем все элементы предыдущего экрана
        for widget in self.winfo_children():
            widget.destroy()

        # Уменьшаем отступы в main_frame
        self.main_frame = ttk.Frame(self, padding="0")  # Убираем или уменьшаем отступы
        self.main_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        notifications = self.get_notifications_today()
        schedule = self.get_work_schedule_by_id()

        self.display_schedule(schedule)

        self.left_frame = ttk.Frame(self)  # Уменьшаем отступы
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, pady=(0, 1), padx=(5, 0))

        self.create_notifications_area(notifications)

        self.timer_running = False
        self.finish_break_button = None
        self.late_timer_running = False

        self.break_time = self.get_break_time_by_employee_id()

        # Уменьшаем отступы в правом и левом фреймах
        self.right_frame = ttk.Frame(self)  # Уменьшаем отступы
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(0, 0))

        # Создаем кнопки
        self.create_admin_buttons()

        # Создаем рамку для всего блока информации о пользователе и таймера
        right_outer_frame = tk.Frame(self.right_frame, bd=2, relief=tk.RIDGE)
        right_outer_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True, padx=10, pady=(10, 10))
        # Заголовок для правой части (имя, фамилия, email)

        right_text_outer_frame = tk.Frame(self.right_frame)
        right_text_outer_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=(6, 0))

        user_info_label = tk.Label(right_text_outer_frame,
                                   text=f"{self.user['surname']} "
                                        f"{self.user['name']} "
                                        f"{self.user['patronymic']}"
                                        + '\n' + self.user["work_email"],
                                   font=("Helvetica", 16, 'bold'))

        user_info_label.pack(anchor='n', pady=(0, 0), side=tk.TOP)  # Уменьшаем pady для меньших отступов

        # Фрейм для информации о пользователе
        self.user_info_container = tk.Frame(right_outer_frame)
        self.user_info_container.pack(fill=tk.BOTH, expand=True, padx=0, pady=2, side=tk.TOP)

        # Инициализация таймера
        self.break_time_minutes = self.break_time.break_time_min  # Получаем минуты из объекта BreakTime
        self.break_time_seconds = self.break_time_minutes * 60  # Переводим в секунды
        self.break_time_seconds = self.break_time_seconds + self.break_time.break_time_sec

        self.late_minutes = self.break_time.penalty_time_min
        self.late_seconds = self.late_minutes * 60
        self.late_seconds = self.late_seconds + self.break_time.penalty_time_sec

        self.finish_break_button = ttk.Button(right_outer_frame, text="Закончить Перерыв",
                                              command=self.finish_break)
        self.finish_break_button.pack(side=tk.BOTTOM, pady=(0, 20))

        # Изначально кнопка "Закончить Перерыв" неактивна
        self.finish_break_button.config(state=tk.DISABLED)

        self.create_timer()  # Создадим таймер при инициализации

    def create_timer(self):
        # Создаем фрейм для таймера
        outer_timer_container = tk.Frame(self.user_info_container, highlightthickness=0, highlightbackground="gray",
                                         bd=1, relief=tk.RAISED, bg='gray')
        outer_timer_container.pack(side=tk.TOP, pady=(15, 10), padx=(60, 60))  # Отступы вокруг таймера

        timer_container = tk.Frame(outer_timer_container, highlightthickness=1, bd=1, relief=tk.RAISED,
                                   highlightbackground="lightgray")
        timer_container.pack(expand=True, fill=tk.BOTH, pady=(15, 10), padx=(60, 60))  # Отступы вокруг таймера

        # Отображаем таймер на экране
        if self.break_time_seconds > 0:
            minutes, seconds = divmod(self.break_time_seconds, 60)
            time_string = f"{minutes:02d}:{seconds:02d}"
            self.timer_label = tk.Label(timer_container, text=time_string, font=("Helvetica", 24))
            self.timer_label.grid(row=0, column=0, sticky='nsew')
        else:
            minutes, seconds = divmod(self.late_seconds, 60)
            time_string = f"{minutes:02d}:{seconds:02d}"
            self.timer_label = tk.Label(timer_container, text=time_string, font=("Helvetica", 24))
            self.timer_label.config(fg='red')
            self.timer_label.grid(row=0, column=0, sticky='nsew')

    def update_timer(self):
        if self.timer_running:
            if self.break_time_seconds > 0:
                minutes, seconds = divmod(self.break_time_seconds, 60)
                time_string = f"{minutes:02d}:{seconds:02d}"
                self.timer_label.config(text=time_string)
                self.break_time_seconds -= 1
                self.after(1000, self.update_timer)  # Запланировать обновление через 1 секунду
            else:
                # Заканчивается первый таймер, запускаем таймер задержки
                self.timer_running = False
                self.late_timer_running = True
                minutes, seconds = divmod(self.late_seconds, 60)
                time_string = f"{minutes:02d}:{seconds:02d}"
                self.timer_label.config(text=time_string, fg='red')
                self.after(1000, self.update_timer)  # Запланировать обновление через 1 секунду

        elif self.late_timer_running:
            # Обновляем таймер задержки
            self.late_seconds += 1  # Увеличиваем счетчик задержки
            self.late_minutes, seconds = divmod(self.late_seconds, 60)
            time_string = f"{self.late_minutes:02d}:{seconds:02d}"
            self.timer_label.config(text=time_string, fg='red')
            self.after(1000, self.update_timer)  # Запланировать обновление через 1 секунду

    def start_break(self):
        if self.break_time_seconds or self.break_time_minutes:
            self.timer_running = True
            self.update_timer()
            self.set_buttons_state(False)  # Отключаем все кнопки, кроме "Закончить перерыв"
        else:
            self.late_timer_running = True
            self.update_timer()
            self.set_buttons_state(False)  # Отключаем все кнопки, кроме "Закончить перерыв"

        self.other_logic()

    def other_logic(self):
        pass

    def finish_break(self):

        self.timer_running = False
        self.late_timer_running = False  # Останавливаем таймер задержки


        # Получаем оставшиеся минуты и секунды
        remaining_minutes = self.break_time_seconds // 60
        remaining_seconds = self.break_time_seconds % 60  # Вычисляем оставшиеся секунды

        # Получаем время задержки
        late_minutes = self.late_minutes
        late_seconds = self.late_seconds

        # Сохраняем задержку в базу данных
        self.set_break_time_and_penalty_time_to_employee_id_and_date(remaining_minutes, remaining_seconds,
                                                                     late_minutes, late_seconds)

        self.set_buttons_state(True)  # Включаем все кнопки при завершении перерыва

    def set_buttons_state(self, state: bool):
        """Управляет состоянием кнопок: активные или неактивные."""
        state_str = tk.NORMAL if state else tk.DISABLED
        self.finish_break_button.config(state=tk.NORMAL) if not state\
            else self.finish_break_button.config(state=tk.DISABLED)
        for widget in self.button_frame.winfo_children():
            widget.config(state=state_str)  # Устанавливаем состояние каждой кнопки

    def create_user_buttons(self):
        self.button_frame = ttk.Frame(self.right_frame, padding="5")
        self.button_frame.pack(side=tk.BOTTOM, pady=(5, 0), padx=(122, 122))

        # Кнопка "Начать Перерыв"
        self.break_button = ttk.Button(self.button_frame, text="Начать Перерыв", command=self.start_break)
        self.break_button.pack(side=tk.LEFT, padx=5, pady=(0, 5))

        # Кнопка "Назад"
        back_button = ttk.Button(self.button_frame, text="Выйти из Системы",
                                 command=self.ask_before_display_login_screen)
        back_button.pack(side=tk.LEFT, padx=5, pady=(0, 5))
    def create_admin_buttons(self):
        self.button_frame = ttk.Frame(self.right_frame, padding="5")
        self.button_frame.pack(side=tk.BOTTOM, pady=(5, 0))

        # Кнопка "Начать Перерыв"
        self.break_button = ttk.Button(self.button_frame, text="Начать Перерыв", command=self.start_break)
        self.break_button.pack(side=tk.LEFT, padx=5, pady=(0, 5))

        graphs_button = ttk.Button(self.button_frame, text="Графики",
                                   command=self.display_work_schedule_management_screen)
        graphs_button.pack(side=tk.LEFT, padx=5, pady=(0, 5))

        registration_button = ttk.Button(self.button_frame, text="Регистрация Сотрудника",
                                         command=self.register_employee_screen)
        registration_button.pack(side=tk.LEFT, padx=5, pady=(0, 5))

        # Кнопка "Назад"
        back_button = ttk.Button(self.button_frame, text="Выйти из Системы",
                                 command=self.ask_before_display_login_screen)
        back_button.pack(side=tk.LEFT, padx=5, pady=(0, 5))

    def set_break_time_and_penalty_time_to_employee_id_and_date(self, break_time_min, break_time_sec,
                                                                penalty_time_min=0, penalty_time_sec=0):
        controller = ControllerFactory.create_break_time_controller()
        return controller.set_break_time_and_penalty_time_to_employee_id_and_date(self.user['id'],
                                                                                  break_time_min, break_time_sec,
                                                                                  penalty_time_min, penalty_time_sec)

    def get_break_time_by_employee_id(self):
        controller = ControllerFactory.create_break_time_controller()
        return controller.get_break_time_by_employee_id(self.user['id'])

    def display_schedule(self, schedule):
        """ Отображает расписание в текстовом поле. """

        # Создаем рамку для всего расписания
        schedule_outer_frame = tk.Frame(self.main_frame, bd=2, relief=tk.RIDGE)
        schedule_outer_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(10,0))

        # Создаем фрейм для строки с днями недели
        self.schedule_text_area = tk.Frame(schedule_outer_frame)
        self.schedule_text_area.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Заголовок рамки "Расписание"
        title_label = tk.Label(self.schedule_text_area, text="График работы", font=("Helvetica", 16, 'bold'),
                               bg="lightgray", fg="black")
        title_label.grid(row=0, column=0, columnspan=7, pady=(0, 5), sticky="nsew")

        # Дни недели и их времена
        days = [
            ("Понедельник", schedule.monday_start, schedule.monday_end),
            ("Вторник", schedule.tuesday_start, schedule.tuesday_end),
            ("Среда", schedule.wednesday_start, schedule.wednesday_end),
            ("Четверг", schedule.thursday_start, schedule.thursday_end),
            ("Пятница", schedule.friday_start, schedule.friday_end),
            ("Суббота", schedule.saturday_start, schedule.saturday_end),
            ("Воскресенье", schedule.sunday_start, schedule.sunday_end)
        ]

        # Строка с днями недели и их временем
        for i, (day, start, end) in enumerate(days):
            day_frame = tk.Frame(self.schedule_text_area, bd=1, relief=tk.RAISED, bg="lightgray")
            day_frame.grid(row=1, column=i, padx=5, pady=5, sticky="nsew")

            # Заголовок дня
            day_label = tk.Label(day_frame, text=day, font=("Helvetica", 11, 'bold'), fg="black")
            day_label.pack(side=tk.TOP, anchor='center', padx=5, pady=5)

            # Фрейм с временем
            time_frame = tk.Frame(day_frame, bd=1, relief=tk.SUNKEN, bg="gray")
            time_frame.pack(side=tk.TOP, padx=5, pady=2)

            # Метка с временем
            if start != "-" and end != "-":
                time_label = tk.Label(time_frame, text=f"{start} - {end}", font=("Helvetica", 11), fg="white",
                                      bg="gray")
            else:
                time_label = tk.Label(time_frame, text="       —       ", font=("Helvetica", 11), fg="white", bg="gray")

            time_label.pack(padx=5, pady=2)

            # Для равномерного распределения колонок
            self.schedule_text_area.grid_columnconfigure(i, weight=1)

        # Для того чтобы фрейм заполнил всю ширину
        self.schedule_text_area.grid_rowconfigure(1, weight=1)

    def create_notifications_area(self, notifications):
        notifications_label = tk.Label(self.left_frame, text="Уведомления",
                                       font=("Helvetica", 16, "bold"), width=25)
        notifications_label.pack(anchor='nw', pady=(5, 5))

        notifications_container = tk.Frame(self.left_frame, relief=tk.RIDGE,
                                           borderwidth=2, bg="#D3D3D3")  # Removed width
        notifications_container.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        canvas = tk.Canvas(notifications_container)
        scrollbar = tk.Scrollbar(notifications_container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#D3D3D3")

        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set, width=75)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.display_notifications(notifications, scrollable_frame)

    def display_notifications(self, notifications, container):
        for notification in notifications:
            notification_frame = tk.Frame(container, relief=tk.RAISED, borderwidth=2,
                                          highlightthickness=1, highlightbackground="gray",
                                          bg=("green" if notification.status == 1 else "red"))
            notification_frame.config(width=0)
            notification_frame.pack(fill=tk.X, padx=(4, 2), pady=2)

            formatted_seconds = f"{notification.seconds:02}"

            # Frame for date and time (white background with black text)
            datetime_frame = tk.Frame(notification_frame, relief=tk.GROOVE, borderwidth=1, bg="white")
            datetime_frame.pack(side=tk.LEFT, padx=(10, 5), pady=(5, 10), fill=tk.Y)

            datetime_label = tk.Label(datetime_frame, text=f"{notification.date} "
                                                           f"{notification.time}"
                                                           f":{formatted_seconds}",
                                      font=("Helvetica", 11, "bold"), bg=datetime_frame["bg"], fg="black")
            datetime_label.pack(pady=(5, 0))

            # Frame for message text
            message_frame = tk.Frame(notification_frame, bg=notification_frame["bg"])
            message_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 10), pady=(5, 5))

            message_label = tk.Label(message_frame, text=notification.text, justify="center", anchor="center",
                                     font=("Helvetica", 11, "bold"), wraplength=200, bg=notification_frame["bg"],
                                     fg="white", width=18)  # Text color set to white
            message_label.pack(fill=tk.X)

    def add_exit_notification(self):
        controller = ControllerFactory.create_notifications_controller()
        return controller.add_exit_notification(self.user)

    def get_notifications_today(self):
        controller = ControllerFactory.create_notifications_controller()
        return controller.get_notifications_today_by_employee_id(self.user['id'])

    def display_work_schedule_management_screen(self):
        user = self.user
        self.destroy()
        from factories.view_factory import ViewFactory
        work_schedule_management_view = ViewFactory.work_schedule_management_view()
        work_schedule_management_view.display_work_schedule_management_screen(user)

    def get_work_schedule_by_id(self):
        controller = ControllerFactory.create_work_schedule_management_controller()
        return controller.get_work_schedule_by_id(self.user['schedule_id'])

    def register_employee_screen(self):
        user = self.user
        self.destroy()
        from factories.view_factory import ViewFactory
        employee_management_view = ViewFactory.create_employee_management_view()
        employee_management_view.register_employee_screen(user)

    def ask_before_display_login_screen(self):
        self.attributes('-topmost', False)
        if messagebox.askyesno("Выход из системы", "Вы точно желаете выйти из системы?!"):
            self.add_exit_notification()
            self.display_login_screen()  # Закрываем приложение, если пользователь выбрал "Да"

        else:
            self.attributes('-topmost', True)

    def display_login_screen(self):
        self.destroy()
        from factories.view_factory import ViewFactory
        ViewFactory.create_authentication_view().display_login_screen()

