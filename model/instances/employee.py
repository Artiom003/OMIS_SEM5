from model.instances.role import Role
import uuid


class Employee:
    def __init__(self,
                 id: uuid.UUID,
                 password: str,
                 name: str,
                 surname: str,
                 patronymic: str,
                 work_email: str,
                 role: Role,
                 schedule_id: uuid.UUID):

        self._id = id
        self._password = password
        self._name = name
        self._surname = surname
        self._patronymic = patronymic
        self._work_email = work_email
        self._role = role
        self._schedule_id = schedule_id

    @property
    def id(self) -> uuid.UUID:
        return self._id

    @property
    def password(self) -> str:
        return self._password

    @property
    def name(self) -> str:
        return self._name

    @property
    def surname(self) -> str:
        return self._surname

    @property
    def patronymic(self) -> str:
        return self._patronymic

    @property
    def work_email(self) -> str:
        return self._work_email

    @property
    def role(self) -> Role:
        return self._role

    @property
    def schedule_id(self) -> uuid.UUID:
        return self._schedule_id

    @password.setter
    def password(self, value: str):
        self._password = value

    @name.setter
    def name(self, value: str):
        self._name = value

    @surname.setter
    def surname(self, value: str):
        self._surname = value

    @patronymic.setter
    def patronymic(self, value: str):
        self._patronymic = value

    @work_email.setter
    def work_email(self, value: str):
        self._work_email = value

    @role.setter
    def role(self, value: Role):
        self._role = value

    @schedule_id.setter
    def schedule_id(self, value: uuid.UUID):
        self._schedule_id = value
