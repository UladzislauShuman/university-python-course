"""
модуль для обработки данных студентов.

здесь находятся функции для добавления, удаления, сортировки,
расчета статистики и других операций со списком студентов.
"""

from typing import List, Dict, Any
from lab.models import Student
from lab.errors import DataValidationError, DuplicateStudentIdError, StudentNotFoundError

def find_student_by_id(students, student_id):
    """
    находит студента по ID
    
    возвращает объект Student или None, если не найден.
    """
    student_to_find = None  
    for student in students:
        if student.id == student_id:
            student_to_find = student
            break 
    
    return student_to_find

def add_student(students: List[Student], new_student: Student):
    """
    добавляет нового студента в список, проверяя на дубликат id.
    
    изменяет переданный список `students`
    """
    if find_student_by_id(students=students, student_id=new_student.id) != None:
        raise DuplicateStudentIdError(f"студент с id={new_student.id} уже существует.")
    students.append(new_student)


def remove_student_by_id(students: List[Student], student_id: int):
    """
    удаляет студента из списка по id.
    
    изменяет переданный список `students`
    """
    student_to_remove = find_student_by_id(students=students, student_id=student_id)
    if student_to_remove:
        students.remove(student_to_remove)
    else:
        raise StudentNotFoundError(f"студент с id={student_id} не найден.")


def update_student_grades(students: List[Student], student_id: int, new_grades: List[int]):
    """
    обновляет оценки студента по id.
    
    изменяет переданный список `students`
    """
    student_to_update = find_student_by_id(students=students, student_id=student_id)
    if student_to_update:
        for grade in new_grades:
            if not isinstance(grade, int) or not (0 <= grade <= 100):
                raise DataValidationError(f"некорректная оценка: '{grade}'.")
        student_to_update.grades = new_grades
    else:
        raise StudentNotFoundError(f"студент с id={student_id} не найден.")


def sort_students(students: List[Student], by: str) -> List[Student]:
    """
    сортирует список студентов по ключу ('avg', 'name', 'id').
    
    возвращает новый отсортированный список, не изменяя исходный.
    """
    if by == "avg":
        return sorted(students, key=lambda s: (-s.average, s.name.lower()))
    if by == "name":
        return sorted(students, key=lambda s: s.name.lower())
    if by == "id":
        return sorted(students, key=lambda s: s.id)
    raise DataValidationError(f"неизвестный ключ сортировки: '{by}'. доступны: avg, name, id.")


def get_group_statistics(students: List[Student]) -> Dict[str, Any]:
    """
    рассчитывает групповую статистику.
    """
    if not students:
        return {
            "student_count": 0,
            "overall_average": 0.0,
            "best_student": None,
            "worst_student": None,
        }

    all_grades = [g for s in students for g in s.grades]
    overall_avg = sum(all_grades) / len(all_grades) if all_grades else 0.0

    sorted_by_avg = sort_students(students, by="avg")
    
    return {
        "student_count": len(students),
        "overall_average": overall_avg,
        "best_student": sorted_by_avg[0],
        "worst_student": sorted_by_avg[-1],
    }


def export_top_n_students_to_csv_string(students: List[Student], n: int) -> str:
    """
    создает строковое представление csv для топ-n студентов.
    """
    sorted_by_avg = sort_students(students, by="avg")
    top_students = sorted_by_avg[:n]

    csv_lines = ["id,name,average,grades"]
    for s in top_students:
        grades_str = " ".join(map(str, s.grades))
        avg_str = f"{s.average:.2f}"
        csv_lines.append(f"{s.id},{s.name},{avg_str},{grades_str}")

    return "\n".join(csv_lines)