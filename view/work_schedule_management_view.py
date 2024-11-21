from view.base_view import BaseView
from view.center_window_helper import CenterWindowHelper
from factories.controller_factory import ControllerFactory

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from model.exceptions.custom_exceptions import *
import re


class WorkScheduleManagementView(BaseView):

    def add_schedule_screen(self):
        w, h = 300, 352
        self.geometry(f"{w}x{h}")
        CenterWindowHelper.center_window(self, w, h)

        for widget in self.winfo_children():
            widget.destroy()

        style = ttk.Style()
        style.configure("Gray.TFrame", background="#D3D3D3")

        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        title_label = ttk.Label(main_frame, text="Добавить график", font=("Helvetica", 16))
        title_label.pack(pady=(0, 10))

        day_labels = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]
        self.entries = []

        for day in day_labels:
            frame = ttk.Frame(main_frame, style="Gray.TFrame", padding="5")
            frame.pack(fill=tk.X, pady=(5, 0))

            centered_frame = ttk.Frame(frame)
            centered_frame.pack(side=tk.LEFT, expand=True)

            day_label = ttk.Label(centered_frame, text=day + ":", font=("Helvetica", 12))
            day_label.pack(side=tk.LEFT)

            entry = ttk.Entry(frame, width=20)
            entry.pack(side=tk.LEFT, padx=(5, 0))
            self.entries.append(entry)

            placeholder_text = "HH:MM-HH:MM"
            entry.config(foreground="gray")  # Set initial text color to gray
            entry.configure(justify='center')  # Center the text

            entry.insert(0, placeholder_text)
            entry.bind("<FocusIn>",
                       lambda e, entry=entry, placeholder=placeholder_text: self.on_entry_click(entry, placeholder))
            entry.bind("<FocusOut>",
                       lambda e, entry=entry, placeholder=placeholder_text: self.on_focusout(entry, placeholder))

        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=(10, 0))

        add_button = ttk.Button(button_frame, text="Добавить График",
                                command=self.add_schedule)
        add_button.pack(side=tk.LEFT, padx=(0, 10))

        back_button = ttk.Button(button_frame, text="Назад", command=self.work_schedule_management_screen)
        back_button.pack(side=tk.LEFT)

    # Метод для обработки события потери фокуса
    def on_focusout(self, entry, placeholder_text):
        if not entry.get():
            entry.insert(0, placeholder_text)
            entry.config(foreground='gray')  # Исправлено на foreground

    # Метод для обработки события получения фокуса
    def on_entry_click(self, entry, placeholder_text):
        if entry.get() == placeholder_text:
            entry.delete(0, tk.END)
            entry.config(foreground='black')  # Меняем цвет текста на черный

    def add_schedule(self):

        schedule_data = {}
        empty_fields = True
        invalid_format = False

        for i, entry in enumerate(self.entries):
            value = entry.get().replace(" ", "")
            if value:
                if value == 'HH:MM-HH:MM':
                    schedule_data[i] = "-"  # Записываем "-" если поле не заполнено
                else:
                    empty_fields = False
                    try:
                        if not self.validate_time_format(value):
                            invalid_format = True
                            break

                        time1, time2 = value.split('-')
                        hours1, minutes1 = map(int, time1.split(':'))
                        hours2, minutes2 = map(int, time2.split(':'))

                        # Проверка на логичность времени (конец должен быть позже начала)
                        if (hours2, minutes2) <= (hours1, minutes1):
                            invalid_format = True
                            break

                        schedule_data[i] = value

                    except ValueError:
                        invalid_format = True
                        break

        if empty_fields:
            messagebox.showerror("Ошибка", "Все поля не могут быть пустыми!")
            return
        try:

            if invalid_format:
                raise WorkScheduleException

            # Запись данных в 14 переменных
            monday_start, monday_end = schedule_data.get(0, "-").replace(" ", "").split('-') \
                if schedule_data.get(0, "-") != "-" else ("-", "-")
            tuesday_start, tuesday_end = schedule_data.get(1, "-").replace(" ", "").split('-') \
                if schedule_data.get(1, "-") != "-" else ("-", "-")
            wednesday_start, wednesday_end = schedule_data.get(2, "-").replace(" ", "").split('-') \
                if schedule_data.get(2, "-") != "-" else ("-", "-")
            thursday_start, thursday_end = schedule_data.get(3, "-").replace(" ", "").split('-') \
                if schedule_data.get(3, "-") != "-" else ("-", "-")
            friday_start, friday_end = schedule_data.get(4, "-").replace(" ", "").split('-') \
                if schedule_data.get(4, "-") != "-" else ("-", "-")
            saturday_start, saturday_end = schedule_data.get(5, "-").replace(" ", "").split('-') \
                if schedule_data.get(5, "-") != "-" else ("-", "-")
            sunday_start, sunday_end = schedule_data.get(6, "-").replace(" ", "").split('-') \
                if schedule_data.get(6, "-") != "-" else ("-", "-")

            controller = ControllerFactory.create_work_schedule_management_controller()
            controller.add_work_schedule(monday_start, monday_end,
                                         tuesday_start, tuesday_end,
                                         wednesday_start, wednesday_end,
                                         thursday_start, thursday_end,
                                         friday_start, friday_end,
                                         saturday_start, saturday_end,
                                         sunday_start, sunday_end)

        except WorkScheduleExistsException:
            messagebox.showerror("Ошибка", "Данный график уже существует!")
            return
        except WorkScheduleException:
            messagebox.showerror("Ошибка", "Неверный ввод в одном или нескольких полях!")
            return
        except Exception:
            messagebox.showerror("Ошибка", "Неизвестная ошибка!")
            return

        messagebox.showinfo("Успех", "График успешно добавлен!")
        self.work_schedule_management_screen()

    def validate_time_format(self, time_str):
        """Проверяет формат времени HH:MM-HH:MM."""
        pattern = re.compile(r'^(?:[01]\d|2[0-3]):[0-5]\d-(?:[01]\d|2[0-3]):[0-5]\d$')
        return bool(pattern.match(time_str))
    def display_work_schedule_management_screen(self, user):
        self.user = user
        w, h = 655, 415  # Увеличиваем высоту для лучшего размещения
        self.geometry(f"{w}x{h}")

        # Центрируем окно
        CenterWindowHelper.center_window(self, w, h)
        self.attributes('-topmost', True)

        # Создаем контейнеры для разделения экрана
        self.left_frame = ttk.Frame(self, padding="10")
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, pady=(0, 6))

        self.right_frame = ttk.Frame(self, padding="5")
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Оборачиваем левую часть в рамку
        left_frame_container = ttk.Frame(self.left_frame, relief=tk.RIDGE, borderwidth=2, padding="5")
        left_frame_container.pack(fill=tk.BOTH, expand=True)

        # Заголовок для левой части с сотрудниками
        employees_label = ttk.Label(left_frame_container, text="Список сотрудников", font=("Helvetica", 16, 'bold'))
        employees_label.pack(anchor='center', padx=5, pady=(0, 10))

        # Создаем рамку для Listbox и Scrollbar
        listbox_frame = ttk.Frame(left_frame_container)  # Обернем Listbox в рамку
        listbox_frame.pack(fill=tk.BOTH, expand=True)

        # Список сотрудников
        self.employees_listbox = tk.Listbox(listbox_frame, height=20, width=40)
        self.employees_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Создаем и настраиваем Scrollbar
        scrollbar = ttk.Scrollbar(listbox_frame)  # Создаем Scrollbar
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Привязываем Scrollbar к Listbox
        self.employees_listbox.config(yscrollcommand=scrollbar.set)  # Привязка
        scrollbar.config(command=self.employees_listbox.yview)  # Привязка Scrollbar к Listbox

        # Привязываем событие на выбор сотрудника
        self.employees_listbox.bind("<<ListboxSelect>>", self.on_employee_select)

        # Загружаем сотрудников
        self.employees = self.get_employees()  # Храним список сотрудников
        self.populate_employee_list()  # Заполняем список employees_listbox

        # Отключаем тулбар
        self.overrideredirect(True)

        # По умолчанию выбираем первого сотрудника
        if self.employees_listbox.size() > 0:
            self.employees_listbox.selection_set(0)  # Выбор первого элемента
            self.employees_listbox.activate(0)  # Активируем первый элемент
            self.on_employee_select()  # Загружаем расписание для первого сотрудника

    def create_buttons(self):

        """ Создает кнопки для управления расписанием. """
        # Создаем рамку для кнопок
        button_frame = ttk.Frame(self.right_frame, style="Gray.TFrame", padding="10")
        button_frame.pack(side=tk.BOTTOM, pady=(0, 0))

        # Кнопка "Добавить расписание"
        add_schedule_button = ttk.Button(button_frame, text="Добавить График",
                                        command=self.add_schedule_screen)
        add_schedule_button.pack(side=tk.LEFT, padx=(0, 5))  # Размещаем слева с отступом

        # Кнопка "Назначить расписание"
        assign_schedule_button = ttk.Button(button_frame, text="Назначить График",
                                           command=self.display_assign_schedule_screen)
        assign_schedule_button.pack(side=tk.LEFT, padx=(0, 5))  # Размещаем рядом с отступом

        # Кнопка "Назад"
        back_button = ttk.Button(button_frame, text="Назад",
                                command=self.display_main_screen)
        back_button.pack(side=tk.LEFT, padx=(0, 5))  # Размещаем справа с отступом

    def display_assign_schedule_screen(self):
        selection = self.employees_listbox.curselection()

        if selection:  # Если есть выбранный элемент
            index = selection[0]
            self.employee_id = self.employees[index]['id']  # Получаем ID выбранного сотрудника
            self.selected_employee_name = (f"{self.employees[index]['surname']} {self.employees[index]['name']}"
                                           f" {self.employees[index]['patronymic']} ({self.employees[index]['role']})")

        self.schedules = self.get_work_schedules()
        self.selected_schedule = None

        w, h = 980, 500  # Уменьшаем высоту окна
        self.geometry(f"{w}x{h}")
        CenterWindowHelper.center_window(self, w, h)

        # Уничтожаем все элементы предыдущего экрана
        for widget in self.winfo_children():
            widget.destroy()

        style = ttk.Style()  # Create a Style object

        # Define a style for the frames
        style.configure("Gray.TFrame", background="#D3D3D3") # Light gray
        # style.configure("Green.TFrame", background="green")

        # Создаём основной фрейм для размещения элементов
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Заголовок
        title_label = ttk.Label(main_frame, text="Назначить график", font=("Helvetica", 16, "bold"))
        title_label.pack(pady=(0, 10))

        # Элемент выбора сотрудника (только для отображения)
        employee_label = ttk.Label(main_frame, text=f"Сотрудник: {self.selected_employee_name}",
                                   font=("Helvetica", 14, "bold"))
        employee_label.pack(pady=(0, 10))

        outer_frame = ttk.Frame(main_frame, relief=tk.GROOVE, borderwidth=2)  # Added outer frame
        outer_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))  # Added pady

        scrollable_frame = ttk.Frame(outer_frame)
        scrollable_frame.rowconfigure(0, weight=1)  # Важно для правильного растягивания canvas
        scrollable_frame.columnconfigure(0, weight=1)  # Важно для правильного растягивания canvas
        scrollable_frame.pack(fill=tk.BOTH, expand=True)

        canvas = tk.Canvas(scrollable_frame, borderwidth=0, highlightthickness=0)
        scrollbar_y = ttk.Scrollbar(scrollable_frame, orient='vertical', command=canvas.yview)
        scrollable_content = ttk.Frame(canvas)

        scrollable_content.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.configure(yscrollcommand=scrollbar_y.set, width=700)
        canvas.create_window((0, 0), window=scrollable_content, anchor='nw')

        # Используем grid() для canvas и scrollbar
        canvas.grid(row=0, column=0, sticky="nsew")
        scrollbar_y.grid(row=0, column=1, sticky="ns")


        self.schedule_frames = []
        for schedule in self.schedules:
            frame = ttk.Frame(scrollable_content, style="Gray.TFrame")
            frame.pack(fill=tk.X, padx=(9, 0), pady=(5, 5), side=tk.TOP)

            days_frame = ttk.Frame(frame, style="Gray.TFrame")
            days_frame.pack(side=tk.TOP, fill=tk.X, pady=(4, 0))

            days_labels = [
                ("Пн", schedule.monday_start, schedule.monday_end),
                ("Вт", schedule.tuesday_start, schedule.tuesday_end),
                ("Ср", schedule.wednesday_start, schedule.wednesday_end),
                ("Чт", schedule.thursday_start, schedule.thursday_end),
                ("Пт", schedule.friday_start, schedule.friday_end),
                ("Сб", schedule.saturday_start, schedule.saturday_end),
                ("Вс", schedule.sunday_start, schedule.sunday_end),
            ]

            for day, start, end in days_labels:
                day_frame = ttk.Frame(days_frame, padding="5", relief=tk.RAISED)
                day_frame.grid(row=0, column=days_labels.index((day, start, end)), sticky="nsew", padx=5, pady=2)

                day_label = ttk.Label(day_frame, text=day, font=("Helvetica", 11, 'bold'))
                day_label.grid(row=0, column=0, sticky="w")  # Выравнивание по левому краю

                time_frame = ttk.Frame(day_frame, padding="5", relief=tk.SUNKEN, style="Black.TFrame")
                time_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=2)

                if start != "-" and end != "-":
                    time_label = ttk.Label(time_frame, text=f"{start} - {end}", font=("Helvetica", 8),
                                           foreground="white", background="black", wraplength=80)
                else:
                    time_label = ttk.Label(time_frame, text="         —         ", font=("Helvetica", 8),
                                           foreground="white", background="black")
                time_label.grid(row=0, column=0, sticky="nsew")  # Центрирование с помощью sticky="nsew"

                day_frame.columnconfigure(1, weight=1)  # Равное распределение веса между меткой дня и временем

            select_button = ttk.Button(frame, text="Выбрать", command=lambda sch=schedule: self.select_schedule(sch))
            select_button.pack(side=tk.RIGHT, padx=(0, 5), pady=(3, 5))

            self.schedule_frames.append(frame)

        self.assign_button = ttk.Button(main_frame, text="Назначить График", command=self.assign_schedule)
        self.assign_button.pack(pady=(0, 0))

        self.back_button = ttk.Button(main_frame, text="Назад", command=self.work_schedule_management_screen)
        self.back_button.pack(pady=(10, 0))

    def select_schedule(self, schedule):
        """Метод для выбора расписания."""
        self.selected_schedule = schedule
        tk.messagebox.showinfo("Выбор графика", "График выбран")

    def assign_schedule(self):
        if not self.selected_schedule:
            tk.messagebox.showwarning("Ошибка", "Пожалуйста, выберите график.")
            return

        try:
            # Вызов функции для назначения расписания сотруднику
            self.set_schedule_to_employee(self.selected_schedule.id, self.employee_id)
            tk.messagebox.showinfo("Успех", "График назначен!")
            self.work_schedule_management_screen()

        except Exception as e:
            tk.messagebox.showerror("Ошибка", f"Ошибка назначения графика: {e}")

    def work_schedule_management_screen(self):
        user = self.user
        self.destroy()
        from factories.view_factory import ViewFactory
        work_schedule_management_view = ViewFactory.work_schedule_management_view()
        work_schedule_management_view.display_work_schedule_management_screen(user)

    def display_schedule(self, schedule):
        """ Отображает расписание в текстовом поле. """
        # Очищаем предыдущие рамки расписания, если они есть
        for widget in self.right_frame.winfo_children():
            widget.destroy()

        # Создаем большую рамку для всего расписания
        schedule_outer_frame = tk.Frame(self.right_frame, bd=2, relief=tk.RIDGE)  # Большая рамка
        schedule_outer_frame.pack(fill=tk.BOTH, expand=True, padx=(5, 5), pady=(5, 5))  # Больше отступы для обрамления

        self.schedule_frames = []  # Список для хранения рамок с расписанием
        self.schedule_text_area = tk.Frame(schedule_outer_frame)  # Помещаем текстовое поле внутри более крупной рамки
        self.schedule_text_area.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Заголовок рамки "Расписание"
        title_label = tk.Label(self.schedule_text_area, text="График работы", font=("Helvetica", 16, 'bold'))
        title_label.pack(anchor='n', pady=(0, 0))  # Располагаем заголовок выше

        # Полные названия дней недели
        days = [
            ("Понедельник", schedule.monday_start, schedule.monday_end),
            ("Вторник", schedule.tuesday_start, schedule.tuesday_end),
            ("Среда", schedule.wednesday_start, schedule.wednesday_end),
            ("Четверг", schedule.thursday_start, schedule.thursday_end),
            ("Пятница", schedule.friday_start, schedule.friday_end),
            ("Суббота", schedule.saturday_start, schedule.saturday_end),
            ("Воскресенье", schedule.sunday_start, schedule.sunday_end)
        ]

        # Создаем рамки для каждого дня
        for day, start, end in days:
            day_frame = tk.Frame(self.schedule_text_area, bd=1, relief=tk.RAISED, bg='gray')
            day_frame.pack(fill=tk.X, padx=5, pady=(3, 3))  # Уменьшаем отступы

            # Делаем рамку более узкой
            day_label = tk.Label(day_frame, text=day, font=("Helvetica", 12, 'bold'))
            day_label.pack(side=tk.LEFT, anchor='center', padx=(5, 10), pady=(5, 5))  # Размещаем слева

            # Проверяем, если время не равно "-"
            if start != "-" and end != "-":
                # Создаем дополнительную рамку для времени с черным фоном
                time_frame = tk.Frame(day_frame, bd=1, relief=tk.SUNKEN, bg="black")
                time_frame.pack(side=tk.RIGHT, anchor='e', padx=5, pady=2)  # Размещаем справа

                # Метка для времени с белым текстом
                time_label = tk.Label(time_frame, text=f"{start} - {end}", font=("Helvetica", 12), fg="white",
                                      bg="black")  # Белый текст, черный фон
                time_label.pack(padx=5, pady=2)  # Увеличиваем размер текста внутри
            else:
                # Если время равно "-", просто добавляем пустое пространство
                time_frame = tk.Frame(day_frame, bd=1, relief=tk.SUNKEN, bg="black")
                time_frame.pack(side=tk.RIGHT, anchor='e', padx=5, pady=2)  # Размещаем справа

                # Метка для времени с белым текстом
                time_label = tk.Label(time_frame, text=f"         —         ", font=("Helvetica", 12), fg="white",
                                      bg="black")  # Белый текст, черный фон
                time_label.pack(padx=5, pady=2)  # Увеличиваем размер текста внутри

            self.schedule_frames.append(day_frame)

    def populate_employee_list(self):
        """ Заполняет виджет Listbox списком сотрудников с ФИО и их ролью. """
        self.employees_listbox.delete(0, tk.END)  # Очищаем существующий список
        for employee in self.employees:
            full_name = f"{employee['surname']} {employee['name']} {employee['patronymic']} ({employee['role']})"
            self.employees_listbox.insert(tk.END, full_name)  # Добавляем полное имя и роль сотрудника

    def on_employee_select(self, event=None):
        """ Обрабатывает выбор сотрудника и обновляет расписание. """
        selection = self.employees_listbox.curselection()

        if selection:  # Если есть выбранный элемент
            index = selection[0]

            schedule_id = self.employees[index]['schedule_id']  # Получаем schedule_id для выбранного сотрудника

            # Обновляем текстовое поле с расписанием работы выбранного сотрудника
            schedule = self.get_work_schedule_by_id(schedule_id)  # Получаем расписание по schedule_id

            self.display_schedule(schedule)

            self.create_buttons()
    def display_main_screen(self):
        user = self.user
        self.destroy()
        from factories.view_factory import ViewFactory
        ViewFactory.create_main_view().display_main_screen_administrator(user)

    def get_work_schedule_by_id(self, employee_id):
        controller = ControllerFactory.create_work_schedule_management_controller()
        return controller.get_work_schedule_by_id(employee_id)

    def get_work_schedules(self):
        controller = ControllerFactory.create_work_schedule_management_controller()
        return controller.get_work_schedules()

    def get_employees(self):
        controller = ControllerFactory.create_employee_management_controller()
        return controller.find_all()

    def set_schedule_to_employee(self, schedule_id, employee_id):
        controller = ControllerFactory.create_employee_management_controller()
        controller.set_schedule_to_employee(schedule_id, employee_id)

