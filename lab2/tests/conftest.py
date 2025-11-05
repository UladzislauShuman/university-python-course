"""
файл для общих фикстур
"""

import pytest
from lab.models import Student


@pytest.fixture
def sample_students() -> list[Student]:
    """
    тестовый набор студентов
    с разными средними баллами для тестов сортировки и статистики.
    """
    return [
        Student(id=1, name="Иванов Иван", grades=[80, 90]),      # ср. 85.0
        Student(id=2, name="Петров Петр", grades=[60, 70, 80]),  # ср. 70.0
        Student(id=3, name="Сидорова Анна", grades=[95, 85, 90]) # ср. 90.0
    ]