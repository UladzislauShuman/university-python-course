import pytest
from lab.models import Student
from lab.processing import sort_students, get_group_statistics, export_top_n_students_to_csv_string


@pytest.fixture
def students_for_sorting():
    return [
        Student(id=3, name="Петров Петр", grades=[70, 70]),      # avg: 70.0
        Student(id=1, name="Иванов Иван", grades=[90, 100]),     # avg: 95.0
        Student(id=2, name="Антонова Анна", grades=[90, 100]),   # avg: 95.0 (такой же, как у иванова)
    ]


# --- тесты для сортировки ---

def test_sort_by_id(students_for_sorting):
    """тест сортировки по id."""
    sorted_list = sort_students(students_for_sorting, 'id')
    ids = [s.id for s in sorted_list]
    assert ids == [1, 2, 3]


def test_sort_by_name(students_for_sorting):
    """тест сортировки по имени."""
    sorted_list = sort_students(students_for_sorting, 'name')
    names = [s.name for s in sorted_list]
    assert names == ["Антонова Анна", "Иванов Иван", "Петров Петр"]


def test_sort_by_avg_stable(students_for_sorting):
    """тест стабильной сортировки по среднему баллу."""
    sorted_list = sort_students(students_for_sorting, 'avg')
    names = [s.name for s in sorted_list]
    
    # ожидаемый порядок:
    # 1. Антонова (avg 95.0) - имя 'А'
    # 2. Иванов (avg 95.0) - имя 'И'
    # 3. Петров (avg 70.0)
    # сначала по убыванию среднего балла, потом по имени (a..z)
    assert names == ["Антонова Анна", "Иванов Иван", "Петров Петр"]
    # проверка на чистоту функции
    original_ids = [s.id for s in students_for_sorting]
    assert original_ids == [3, 1, 2]


# --- тесты для статистики ---

def test_group_statistics():
    """тест расчета статистики для группы студентов."""
    students = [
        Student(1, "A", [100]), # avg: 100
        Student(2, "B", [50, 50]), # avg: 50
        Student(3, "C", [70, 80]) # avg: 75
    ]
    stats = get_group_statistics(students)

    assert stats["student_count"] == 3
    # общий средний балл: (100 + 50 + 50 + 70 + 80) / 5 = 70.0
    assert stats["overall_average"] == 70.0
    assert stats["best_student"].name == "A"
    assert stats["worst_student"].name == "B"


def test_group_statistics_empty_list():
    """тест расчета статистики для пустого списка."""
    stats = get_group_statistics([])
    
    assert stats["student_count"] == 0
    assert stats["overall_average"] == 0.0
    assert stats["best_student"] is None
    assert stats["worst_student"] is None


# --- тесты для экспорта ---

def test_export_top_n_students():
    """тест экспорта топ-n студентов в csv-строку."""
    students = [
        Student(1, "A", [60]), # avg: 60
        Student(2, "B", [100]), # avg: 100
        Student(3, "C", [80]), # avg: 80
    ]
    
    csv_string = export_top_n_students_to_csv_string(students, 2)
    lines = csv_string.strip().split('\n')
    
    assert lines[0] == "id,name,average,grades"
    assert len(lines) == 3 # 2 студента и 1 заголовок
    assert lines[1].startswith("2,B,100.00,100")
    assert lines[2].startswith("3,C,80.00,80")