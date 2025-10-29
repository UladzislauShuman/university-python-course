"""
модуль для определения исключений.
"""


class StudentAppException(Exception):
    """базовый класс для всех исключений."""
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

# для ошибок, связанных с файловой системой, таких как "файл не найден"
# или "нет прав на чтение", мы будем использовать встроенные в python исключения
# (FileNotFoundError, PermissionError).