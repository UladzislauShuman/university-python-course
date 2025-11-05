"""
тесты для модуля models.py.
"""
import pytest
from lab.models import Student
from lab.errors import DataValidationError


def test_student_creation_and_average():
    """тест на успешное создание студента и расчет среднего балла."""
    s = Student(id=10, name="Шуман Влад ", grades=[100, 80, 90])
    assert s.id == 10
    assert s.name == "Шуман Влад"
    assert pytest.approx(s.average) == 90.0


def test_student_average_empty_grades():
    """тест расчета среднего для студента без оценок."""
    s = Student(id=1, name="Без Оценок", grades=[])
    assert s.average == 0.0


def test_student_str_representation():
    """тест строкового представления объекта."""
    s = Student(id=1, name="Иван", grades=[80, 90])
    expected_str = "ID: 1, Имя: Иван, Оценки: [80, 90], Средний балл: 85.00"
    assert str(s) == expected_str


@pytest.mark.parametrize("test_id, name, grades, error_msg", [
    (0, "Имя", [], "id студента должен быть положительным"),
    ("1", "Имя", [], "id студента должен быть положительным"),
    (1, "  ", [], "имя студента не может быть пустым"),
    (1, "Имя", "не список", "оценки должны быть представлены в виде списка"),
    (1, "Имя", [101], "оценка должна быть целым числом от 0 до 100"),
    (1, "Имя", [-1], "оценка должна быть целым числом от 0 до 100"),
])
def test_student_creation_invalid_data(test_id, name, grades, error_msg):
    """параметризованный тест на создание студента с невалидными данными."""
    with pytest.raises(DataValidationError) as excinfo:
        Student(id=test_id, name=name, grades=grades)
    assert error_msg in str(excinfo.value)