"""
модуль для определения исключений.
"""


class StudentAppException(Exception):
    """базовый класс для всех исключений этого приложения."""
    pass


class DataValidationError(StudentAppException):
    """вызывается, когда данные не проходят проверку (например, некорректный id или оценка)."""
    pass


class StudentNotFoundError(StudentAppException):
    """вызывается при попытке доступа к студенту по несуществующему id."""
    pass


class DuplicateStudentIdError(StudentAppException):
    """вызывается при попытке добавить студента с id, который уже существует."""
    pass

class FileFormatError(StudentAppException):
    """вызывается при неверном формате файла (например, отсутствуют необходимые колонки)."""
    pass