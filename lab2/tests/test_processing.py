"""
тесты для модуля processing.py.
"""

import pytest
from lab.models import Student
from lab import processing
from lab.errors import DataValidationError, DuplicateStudentIdError, StudentNotFoundError


def test_add_remove_update_logic(sample_students):
    """тестирует добавление, обновление и удаление студентов."""
    students = list(sample_students)
    
    # 1. добавление
    new_student = Student(id=10, name="Новый", grades=[70, 80])
    processing.add_student(students, new_student)
    assert any(s.id == 10 for s in students)

    # 2. попытка добавить дубликат
    with pytest.raises(DuplicateStudentIdError):
        processing.add_student(students, Student(id=10, name="Дубликат", grades=[]))

    # 3. обновление
    processing.update_student_grades(students, 10, [100])
    updated_student = next(s for s in students if s.id == 10)
    assert updated_student.grades == [100]

    # 4. попытка обновить несуществующего студента
    with pytest.raises(StudentNotFoundError):
        processing.update_student_grades(students, 999, [])

    # 5. удаление
    processing.remove_student_by_id(students, 10)
    assert all(s.id != 10 for s in students)

    # 6. попытка удалить несуществующего студента
    with pytest.raises(StudentNotFoundError):
        processing.remove_student_by_id(students, 10)


def test_sort_students(sample_students):
    """тестирует все виды сортировки."""
    # avg disc
    by_avg = processing.sort_students(sample_students, by="avg")
    assert [s.id for s in by_avg] == [3, 1, 2]  # 90.0, 85.0, 70.0

    # name
    by_name = processing.sort_students(sample_students, by="name")
    assert [s.name for s in by_name] == ["Иванов Иван", "Петров Петр", "Сидорова Анна"]

    # id asc
    by_id = processing.sort_students(sample_students, by="id")
    assert [s.id for s in by_id] == [1, 2, 3]

    # неверный ключ
    with pytest.raises(DataValidationError):
        processing.sort_students(sample_students, by="unknown")


def test_group_statistics(sample_students):
    """тестирует расчет статистики для группы."""
    stats = processing.get_group_statistics(sample_students)
    assert stats["student_count"] == 3
    assert pytest.approx(stats["overall_average"]) == (80+90+60+70+80+95+85+90)/8
    assert stats["best_student"].id == 3
    assert stats["worst_student"].id == 2


def test_group_statistics_empty_list():
    """тестирует расчет статистики для пустого списка."""
    stats = processing.get_group_statistics([])
    assert stats["student_count"] == 0
    assert stats["overall_average"] == 0.0
    assert stats["best_student"] is None
    assert stats["worst_student"] is None


def test_export_top_n_students(sample_students):
    """тест экспорта топ-n студентов в csv-строку."""
    csv_string = processing.export_top_n_students_to_csv_string(sample_students, 2)
    lines = csv_string.strip().split('\n')
    
    assert lines[0] == "id,name,average,grades"
    assert len(lines) == 3 # заголовок + 2 студента
    # 1-й: Сидорова (90.00), 2-й: Иванов (85.00)
    assert lines[1].startswith("3,Сидорова Анна,90.00")
    assert lines[2].startswith("1,Иванов Иван,85.00")