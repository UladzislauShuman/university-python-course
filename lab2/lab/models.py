"""
модуль для определения моделей данных.
"""

from dataclasses import dataclass, field
from typing import List
from lab.errors import DataValidationError


@dataclass
class Student:
    """
    класс для представления сущности 'студент'.

    атрибуты:
        id (int): уникальный идентификатор студента.
        name (str): полное имя студента.
        grades (list[int]): список оценок студента (от 0 до 100).
    """
    id: int
    name: str
    grades: List[int] = field(default_factory=list)

    def __post_init__(self):
        """
        валидация данных после метода __init__
        """
        # --- валидация id ---
        if not isinstance(self.id, int) or self.id <= 0:
            raise DataValidationError("id студента должен быть положительным целым числом.")

        # --- валидация имени ---
        if not isinstance(self.name, str) or not self.name.strip():
            raise DataValidationError("имя студента не может быть пустым.")
        self.name = self.name.strip()

        # --- валидация оценок ---
        if not isinstance(self.grades, list):
            raise DataValidationError("оценки должны быть представлены в виде списка.")
        
        for grade in self.grades:
            if not isinstance(grade, int) or not (0 <= grade <= 100):
                raise DataValidationError(f"некорректная оценка: '{grade}'. оценка должна быть целым числом от 0 до 100.")

    @property
    def average(self) -> float:
        """
        вычисляет и возвращает средний балл студента.

        если список оценок пуст, возвращает 0.0.
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