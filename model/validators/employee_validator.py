from model.exceptions.custom_exceptions import (
    FirstNameException,
    LastNameException,
    MiddleNameException,
    WorkEmailException,
    PasswordException,
    KeyCodeException,
)
import re


class EmployeeValidator:
    KeyKode = ('cisco', 'aboba', 'maximloh')

    @staticmethod
    def validate_employee(last_name, first_name, middle_name, work_email, password, key_code=None):

        # Проверка фамилии
        if (not isinstance(last_name, str) or not re.match(r'^[A-Za-zА-Яа-яЁё]+\Z', last_name)
                or not last_name[0].isupper()):
            raise LastNameException

        # Проверка имени
        if (not isinstance(first_name, str) or not re.match(r'^[A-Za-zА-Яа-яЁё]+\Z', first_name)
                or not first_name[0].isupper()):
            raise FirstNameException

        # Проверка отчества
        if (not isinstance(middle_name, str) or not re.match(r'^[A-Za-zА-Яа-яЁё]+\Z', middle_name)
                or not middle_name[0].isupper()):
            raise MiddleNameException

        # Проверка key_code
        if key_code is not None and key_code not in EmployeeValidator.KeyKode:
            raise KeyCodeException

        # Проверка email
        if not re.match(r"[^@]+@[^@]+\.[^@]+", work_email):
            raise WorkEmailException

        # Проверка пароля
        if not isinstance(password, str) or ' ' in password:
            raise PasswordException
