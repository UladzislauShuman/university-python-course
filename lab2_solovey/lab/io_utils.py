"""
модуль для утилит ввода-вывода.

здесь собраны функции для работы с файлами, в частности, для чтения
и записи данных студентов в формате csv.
"""

import csv
from typing import List

from lab.models import Student
from lab.errors import DataValidationError


def load_students_from_csv(filepath: str, has_header: bool) -> List[Student]:
    """
    загружает список студентов из csv-файла.

    аргументы:
        filepath (str): путь к csv-файлу.
        has_header (bool): флаг, указывающий, есть ли в файле строка заголовка.

    возвращает:
        list[Student]: список объектов студентов.

    вызывает:
        FileNotFoundError: если файл не найден.
        DataValidationError: если данные в строке некорректны (например, пустая строка,
                             неверный тип данных, некорректное количество колонок).
    """
    students = []
    try:
        # открываем файл с явным указанием кодировки utf-8 и newline=''
        with open(filepath, mode='r', encoding='utf-8', newline='') as file:
            reader = csv.reader(file)

            # если есть заголовок, пропускаем первую строку
            if has_header:
                try:
                    next(reader)
                except StopIteration:
                    return []

            # обрабатываем каждую строку в файле
            for row_num, row in enumerate(reader, start=2 if has_header else 1):
                # пропускаем пустые строки, которые могут быть в файле
                if not row:
                    continue

                # --- парсинг и валидация строки ---
                if len(row) < 2:
                    raise DataValidationError(f"ошибка в строке {row_num}: недостаточно данных. ожидается как минимум id и имя.")

                student_id_str, name, *grades_str = row

                # парсим id
                try:
                    student_id = int(student_id_str)
                except (ValueError, TypeError):
                    raise DataValidationError(f"ошибка в строке {row_num}: id '{student_id_str}' не является целым числом.")

                # парсим оценки, игнорируя пустые ячейки
                grades = []
                for grade_str in grades_str:
                    # если ячейка пустая, просто пропускаем ее
                    if grade_str.strip() == '':
                        continue
                    try:
                        grade = int(grade_str)
                        grades.append(grade)
                    except (ValueError, TypeError):
                        raise DataValidationError(f"ошибка в строке {row_num}: оценка '{grade_str}' не является целым числом.")
                
                # создаем объект студента (валидация данных произойдет в конструкторе)
                try:
                    student = Student(id=student_id, name=name, grades=grades)
                    students.append(student)
                except DataValidationError as e:
                    # добавляем номер строки к сообщению об ошибке для удобства пользователя
                    raise DataValidationError(f"ошибка в строке {row_num}: {e}")

    except FileNotFoundError:
        raise FileNotFoundError(f"файл не найден по пути: {filepath}")
    except Exception as e:
        # ловим другие возможные ошибки 
        # и оборачиваем их в наше исключение 
        if not isinstance(e, DataValidationError):
             raise IOError(f"произошла ошибка при чтении файла '{filepath}': {e}")
        else:
            raise e

    return students


def save_students_to_csv(filepath: str, students: List[Student], include_header: bool):
    """
    сохраняет список студентов в csv-файл.

    аргументы:
        filepath (str): путь к csv-файлу для сохранения.
        students (list[Student]): список студентов для сохранения.
        include_header (bool): флаг, нужно ли записывать заголовок.
    """
    try:
        # находим максимальное количество оценок у одного студента,
        # чтобы сделать одинаковое количество колонок для всех
        max_grades = 0
        if students:
            max_grades = max(len(s.grades) for s in students)

        with open(filepath, mode='w', encoding='utf-8', newline='') as file:
            writer = csv.writer(file)

            # записываем заголовок, если нужно
            if include_header:
                header = ['id', 'name'] + [f'grade{i+1}' for i in range(max_grades)]
                writer.writerow(header)

            # записываем данные каждого студента
            for student in students:
                row = [student.id, student.name] + student.grades
                row.extend([''] * (max_grades - len(student.grades)))
                writer.writerow(row)

    except IOError as e:
        raise IOError(f"не удалось записать в файл '{filepath}': {e}")