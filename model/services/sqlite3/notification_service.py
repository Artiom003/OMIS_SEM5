from ..base_notification_service import BaseNotificationService


class NotificationService(BaseNotificationService):
    def __init__(self):
        from factories.model_factory import ModelFactory
        self.work_schedule_repository = ModelFactory.create_work_schedule_repository(self.FILE)
        self.notification_repository = ModelFactory.create_notification_repository(self.FILE)

    def add_exit_notification(self, employee):
        import datetime

        work_schedule = self.work_schedule_repository.get_work_schedule_by_id(employee['schedule_id'])

        current_time = datetime.datetime.now()
        current_time_str = current_time.strftime('%H:%M')
        current_date = current_time.strftime('%d.%m.%Y')
        current_day = current_time.weekday()
        current_seconds = current_time.second

        # Список дней недели на русском
        days_of_week_ru = [
            "Понедельник", "Вторник", "Среда", "Четверг",
            "Пятница", "Суббота", "Воскресенье"
        ]
        # Получаем день недели на русском
        day_of_week = days_of_week_ru[current_day]

        # Выбираем соответствующие поля в зависимости от текущего дня недели
        if current_day == 4:  # Пятница
            end_time = work_schedule.friday_end
        elif current_day == 5:  # Суббота
            end_time = work_schedule.saturday_end
        elif current_day == 6:  # Воскресенье
            end_time = work_schedule.sunday_end
        elif current_day == 0:  # Понедельник
            end_time = work_schedule.monday_end
        elif current_day == 1:  # Вторник
            end_time = work_schedule.tuesday_end
        elif current_day == 2:  # Среда
            end_time = work_schedule.wednesday_end
        elif current_day == 3:  # Четверг
            end_time = work_schedule.thursday_end
        else:
            return "Неизвестный день недели"

        # Преобразуем строку времени в datetime для удобства вычислений
        end_time_dt = datetime.datetime.strptime(end_time, '%H:%M') if end_time != '-' else None
        current_time_dt = datetime.datetime.strptime(current_time_str, '%H:%M')

        # Если время выхода больше времени окончания рабочего дня
        if end_time_dt and current_time_dt >= end_time_dt:
            status = 1
            text = f"Успешный выход!\n({day_of_week})"
        # В остальных случаях выход вне графика
        else:
            status = 0
            text = f"Выход вне графика!\n({day_of_week})"

        # Добавляем уведомление
        self.notification_repository.add_notification(employee['id'], current_date,
                                                      current_time_str, current_seconds, text, status)

    def add_entered_notification(self, employee):
        import datetime

        work_schedule = self.work_schedule_repository.get_work_schedule_by_id(employee['schedule_id'])

        current_time = datetime.datetime.now()
        current_time_str = current_time.strftime('%H:%M')
        current_date = current_time.strftime('%d.%m.%Y')
        current_day = current_time.weekday()
        current_seconds = current_time.second

        # Список дней недели на русском
        days_of_week_ru = [
            "Понедельник", "Вторник", "Среда", "Четверг",
            "Пятница", "Суббота", "Воскресенье"
        ]
        # Получаем день недели на русском
        day_of_week = days_of_week_ru[current_day]

        # Выбираем соответствующие поля в зависимости от текущего дня недели
        if current_day == 4:  # Пятница
            start_time = work_schedule.friday_start
            end_time = work_schedule.friday_end
        elif current_day == 5:  # Суббота
            start_time = work_schedule.saturday_start
            end_time = work_schedule.saturday_end
        elif current_day == 6:  # Воскресенье
            start_time = work_schedule.sunday_start
            end_time = work_schedule.sunday_end
        elif current_day == 0:  # Понедельник
            start_time = work_schedule.monday_start
            end_time = work_schedule.monday_end
        elif current_day == 1:  # Вторник
            start_time = work_schedule.tuesday_start
            end_time = work_schedule.tuesday_end
        elif current_day == 2:  # Среда
            start_time = work_schedule.wednesday_start
            end_time = work_schedule.wednesday_end
        elif current_day == 3:  # Четверг
            start_time = work_schedule.thursday_start
            end_time = work_schedule.thursday_end
        else:
            return "Неизвестный день недели"

        # Преобразуем строки времени в datetime для удобства вычислений
        start_time_dt = datetime.datetime.strptime(start_time, '%H:%M') if start_time != '-' else None
        end_time_dt = datetime.datetime.strptime(end_time, '%H:%M') if end_time != '-' else None
        current_time_dt = datetime.datetime.strptime(current_time_str, '%H:%M')

        # Проверяем время пользователя относительно start_time и end_time с учетом буферов в 15 минут
        if start_time_dt and current_time_dt < (start_time_dt - datetime.timedelta(minutes=15)) or \
           end_time_dt and current_time_dt > end_time_dt or \
            start_time_dt is None and end_time_dt is None:
            status = 0
            text = f"Вход в не графика!\n({day_of_week})"

        # Если пользователь приходит в промежутке start_time + 15 минут до end_time - 15 минут
        elif start_time_dt and current_time_dt >= (start_time_dt + datetime.timedelta(minutes=15)) and \
             end_time_dt and current_time_dt <= end_time_dt:
            status = 0
            text = f"Опоздание!\n({day_of_week})"

        # В остальных случаях
        else:
            status = 1
            text = f"С возвращением!\n({day_of_week})"

        # Добавляем уведомление
        self.notification_repository.add_notification(employee['id'], current_date,
                                                      current_time_str, current_seconds, text, status)

    def get_notifications_today_by_employee_id(self, employee_id):

        import datetime

        notifications = self.notification_repository.get_notifications_by_employee_id(employee_id)

        today = datetime.date.today().strftime("%d.%m.%Y")  # Получаем сегодняшнюю дату в формате ДД.ММ.ГГГГ

        # Фильтруем уведомления, оставляя только те, у которых дата сегодняшняя
        today_notifications = [notification for notification in notifications if notification.date == today]

        # Сортируем уведомления по времени и секундам в убывающем порядке
        today_notifications.sort(key=lambda n: (datetime.datetime.strptime(n.time, "%H:%M"), n.seconds),
                                 reverse=True)

        return today_notifications




