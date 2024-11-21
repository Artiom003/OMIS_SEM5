from model.exceptions.my_base_exception import MyBaseException


class FirstNameException(MyBaseException):
    pass


class UserDoesntExistsException(MyBaseException):
    pass


class LastNameException(MyBaseException):
    pass


class UserExistsWithThisEmailException(MyBaseException):
    pass


class LoginException(MyBaseException):
    pass


class MiddleNameException(MyBaseException):
    pass


class WorkEmailException(MyBaseException):
    pass


class PasswordException(MyBaseException):
    pass


class KeyCodeException(MyBaseException):
    pass


class WorkScheduleException(MyBaseException):
    pass


class WorkScheduleExistsException(MyBaseException):
    pass

