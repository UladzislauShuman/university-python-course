import pytest
from lab.models import Student
from lab.errors import DataValidationError


@pytest.fixture
def valid_student():
    return Student(id=1, name="Иван Иванов", grades=[80, 90, 100])


# --- Good ---

def test_student_creation(valid_student):
    """тест на успешное создание студента с корректными данными."""
    assert valid_student.id == 1
    assert valid_student.name == "Иван Иванов"
    assert valid_student.grades == [80, 90, 100]


def test_student_average_calculation(valid_student):
    """тест на правильный расчет среднего балла."""
    assert valid_student.average == 90.0


def test_student_average_no_grades():
    """тест на расчет среднего балла, когда список оценок пуст."""
    student = Student(id=2, name="Петр Петров", grades=[])
    assert student.average == 0.0


def test_student_str_representation(valid_student):
    """тест на строковое представление объекта (метод __str__)."""
    expected_str = "ID: 1, Имя: Иван Иванов, Оценки: [80, 90, 100], Средний балл: 90.00"
    assert str(valid_student) == expected_str


# --- Bad ---

@pytest.mark.parametrize(
    "student_id, name, grades, expected_error_msg",
    [
        # невалидный id
        ("1", "Имя", [90], "id студента должен быть положительным целым числом"),
        (0, "Имя", [90], "id студента должен быть положительным целым числом"),
        (-5, "Имя", [90], "id студента должен быть положительным целым числом"),
        # невалидное имя
        (1, "", [90], "имя студента не может быть пустым"),
        (1, "   ", [90], "имя студента не может быть пустым"),
        # невалидные оценки
        (1, "Имя", "не список", "оценки должны быть представлены в виде списка"),
        (1, "Имя", [101], "оценка должна быть целым числом от 0 до 100"),
        (1, "Имя", [-1], "оценка должна быть целым числом от 0 до 100"),
        (1, "Имя", [80, "90"], "оценка должна быть целым числом от 0 до 100"),
    ]
)
def test_student_creation_with_invalid_data(student_id, name, grades, expected_error_msg):
    """
    параметризованный тест для проверки создания студента с невалидными данными.
    """
    with pytest.raises(DataValidationError) as excinfo:
        Student(id=student_id, name=name, grades=grades)
    assert expected_error_msg in str(excinfo.value)