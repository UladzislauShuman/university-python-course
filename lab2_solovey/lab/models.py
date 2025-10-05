"""
модуль для определения моделей данных.
"""

from .errors import DataValidationError


class Student:
    """
    класс для представления сущности 'студент'.

    атрибуты:
        id (int): уникальный идентификатор студента.
        name (str): полное имя студента.
        grades (list[int]): список оценок студента (от 0 до 100).
    """

    def __init__(self, id: int, name: str, grades: list[int]):
        """
        инициализирует объект студента и проверяет корректность входных данных.

        может вызвать исключение DataValidationError
        """
        # --- валидация id ---
        if not isinstance(id, int) or id <= 0:
            raise DataValidationError("id студента должен быть положительным целым числом.")
        self.id = id

        # --- валидация имени ---
        if not isinstance(name, str) or not name.strip():
            raise DataValidationError("имя студента не может быть пустым.")
        # .strip() убирает пробелы в начале и конце строки
        self.name = name.strip()

        # --- валидация оценок ---
        if not isinstance(grades, list):
            raise DataValidationError("оценки должны быть представлены в виде списка.")
        
        # проверяем, что каждый элемент в списке - это число от 0 до 100
        for grade in grades:
            if not isinstance(grade, int) or not (0 <= grade <= 100):
                raise DataValidationError(f"некорректная оценка: '{grade}'. оценка должна быть целым числом от 0 до 100.")
        self.grades = grades

    @property
    def average(self) -> float:
        """
        вычисляет и возвращает средний балл студента.

        если список оценок пуст, возвращает 0.0
        """
        if not self.grades:
            return 0.0
        return sum(self.grades) / len(self.grades)

    def __str__(self) -> str:
        """
        возвращает удобное для пользователя строковое представление объекта.
        """
        grades_str = ', '.join(map(str, self.grades)) if self.grades else "оценок нет"
        return f"ID: {self.id}, Имя: {self.name}, Оценки: [{grades_str}], Средний балл: {self.average:.2f}"

    def __repr__(self) -> str:
        """
        возвращает строковое представление объекта, которое может быть использовано
        для воссоздания этого объекта.
        """
        return f"Student(id={self.id}, name='{self.name}', grades={self.grades})"