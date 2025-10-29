"""
модуль для обработки данных студентов.

здесь находятся функции для сортировки, расчета статистики и других
операций со списком студентов. эти функции являются "чистыми" (не изменяют исходный список, а возвращают новый)
"""

from typing import List, Dict, Any

from lab.models import Student


def sort_students(students: List[Student], sort_by: str) -> List[Student]:
    """
    сортирует список студентов по заданному ключу.

    аргументы:
        students (list[Student]): список студентов для сортировки.
        sort_by (str): ключ сортировки ('id', 'name', 'avg').

    возвращает:
        list[Student]: новый отсортированный список студентов.
    """
    # создаем копию списка, чтобы не изменять оригинальный
    sorted_list = list(students)

    if sort_by == 'id':
        # сортировка по id (по возрастанию)
        sorted_list.sort(key=lambda s: s.id)
    elif sort_by == 'name':
        # сортировка по имени (лексикографически, a..z)
        sorted_list.sort(key=lambda s: s.name)
    elif sort_by == 'avg':
        # стабильная сортировка: сначала по убыванию среднего балла,
        # а для студентов с одинаковым баллом - по имени (a..z)
        sorted_list.sort(key=lambda s: (-s.average, s.name))
    
    return sorted_list


def get_group_statistics(students: List[Student]) -> Dict[str, Any]:
    """
    рассчитывает групповую статистику по списку студентов.

    аргументы:
        students (list[Student]): список студентов.

    возвращает:
        dict: словарь со статистикой (число студентов, общий средний балл,
              лучший и худший студент по среднему баллу).
    """
    if not students:
        return {
            "student_count": 0,
            "overall_average": 0.0,
            "best_student": None,
            "worst_student": None
        }

    # считаем общее количество оценок и их сумму по всем студентам
    total_grades_sum = 0
    total_grades_count = 0
    for s in students:
        total_grades_sum += sum(s.grades)
        total_grades_count += len(s.grades)

    # вычисляем общий средний балл. если оценок нет вообще, будет 0.0
    overall_average = (total_grades_sum / total_grades_count) if total_grades_count > 0 else 0.0

    # находим лучшего и худшего студента по среднему баллу
    # используем lambda-функцию в качестве ключа для max() и min()
    best_student = max(students, key=lambda s: s.average)
    worst_student = min(students, key=lambda s: s.average)

    return {
        "student_count": len(students),
        "overall_average": overall_average,
        "best_student": best_student,
        "worst_student": worst_student
    }


def export_top_n_students_to_csv_string(students: List[Student], n: int) -> str:
    """
    создает строковое представление csv для топ-n студентов.

    студенты предварительно сортируются по убыванию среднего балла.
    формат колонок: id, name, average, grades (оценки через пробел).

    аргументы:
        students (list[Student]): список студентов.
        n (int): количество студентов для экспорта.

    возвращает:
        str: строка в формате csv.
    """
    # сортируем студентов по убыванию среднего балла
    sorted_by_avg = sort_students(students, 'avg')
    
    # берем срез из первых n студентов
    top_students = sorted_by_avg[:n]

    # используем list comprehension для формирования строк csv
    # начинаем с заголовка
    csv_lines = ["id,name,average,grades"]
    
    for s in top_students:
        grades_str = " ".join(map(str, s.grades))
        avg_str = f"{s.average:.2f}"
        csv_lines.append(f"{s.id},{s.name},{avg_str},{grades_str}")

    # объединяем все строки в одну большую строку с переносами
    return "\n".join(csv_lines)