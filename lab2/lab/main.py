"""
главный модуль приложения.

содержит консольный интерфейс пользователя (cli) и является точкой входа.
"""

import sys
from typing import List

from lab.models import Student
from lab import io_utils
from lab import processing
from lab.errors import StudentAppException, DataValidationError


def print_menu():
    """выводит на экран консольное меню."""
    print("\n--- Меню управления списком студентов ---")
    print("1. Загрузить студентов из CSV")
    print("2. Сохранить студентов в CSV")
    print("3. Показать всех студентов")
    print("4. Добавить студента")
    print("5. Удалить студента по ID")
    print("6. Обновить оценки студента по ID")
    print("7. Показать статистику по группе")
    print("8. Экспорт ТОП-N студентов в CSV")
    print("9. Сортировать и показать студентов")
    print("0. Выход")


def press_enter_to_continue():
    """приостанавливает выполнение программы до нажатия enter."""
    input("Нажмите Enter, чтобы продолжить...")


def show_students(students: List[Student]):
    """отображает список студентов в консоли."""
    if not students:
        print("Список студентов пуст.")
        return
    print("\n--- Список студентов ---")
    for s in students:
        print(s)


# --- действия для каждого пункта меню ---

def action_load(students: List[Student]) -> List[Student]:
    """действие: загрузка студентов из файла."""
    path = input("Введите путь к CSV файлу (например, data/students.csv): ").strip()
    if not path.lower().endswith('.csv'):
        print("Ошибка: файл должен иметь расширение .csv")
        return students
    
    has_header = input("Файл содержит заголовок? (y/n): ").lower() == 'y'
    try:
        loaded_students = io_utils.load_students_from_csv(path, has_header)
        print(f"Успешно загружено {len(loaded_students)} студентов.")
        return loaded_students
    except FileNotFoundError:
        print(f"Ошибка: файл не найден по пути '{path}'")
    except PermissionError:
        print(f"Ошибка: нет прав на чтение файла '{path}'")
    except StudentAppException as e:
        print(f"Ошибка формата данных в файле: {e}")
    return students # в случае ошибки возвращает исходный список


def action_save(students: List[Student]):
    """действие: сохранение студентов в файл."""
    if not students:
        print("Список студентов пуст. Нечего сохранять.")
        return
    
    path = input("Введите путь для сохранения CSV файла: ").strip()
    if not path.lower().endswith('.csv'):
        print("Ошибка: файл должен иметь расширение .csv")
        return

    include_header = input("Включить заголовок в файл? (y/n): ").lower() == 'y'
    try:
        io_utils.save_students_to_csv(path, students, include_header)
        print(f"Данные успешно сохранены в файл '{path}'")
    except PermissionError:
        print(f"Ошибка: нет прав на запись в файл '{path}'")
    except IOError as e:
        print(f"Ошибка записи в файл: {e}")


def action_add(students: List[Student]):
    """действие: добавление нового студента."""
    try:
        new_id = int(input("Введите ID нового студента: "))
        name = input("Введите ФИО студента: ").strip()
        grades_str = input("Введите оценки через запятую (например, 80,95,78): ")
        
        grades = [int(g.strip()) for g in grades_str.split(',') if g.strip()]
        
        new_student = Student(id=new_id, name=name, grades=grades)
        processing.add_student(students, new_student)
        print(f"Студент '{name}' успешно добавлен.")
    except ValueError:
        print("Ошибка ввода: ID и оценки должны быть целыми числами.")
    except StudentAppException as e:
        print(f"Ошибка: {e}")


def action_remove(students: List[Student]):
    """действие: удаление студента."""
    if not students:
        print("Список студентов пуст. Некого удалять.")
        return
    try:
        del_id = int(input("Введите ID студента для удаления: "))
        if del_id < 0:
            raise DataValidationError("ID студента должно быть целым положительным числом")
        processing.remove_student_by_id(students, del_id)
        print(f"Студент с ID {del_id} успешно удален.")
    except ValueError:
        print("Ошибка ввода: ID должен быть целым числом.")
    except StudentAppException as e:
        print(f"Ошибка: {e}")


def action_update(students: List[Student]):
    """действие: обновление оценок студента."""
    if not students:
        print("Список студентов пуст. Некого обновлять.")
        return
    try:
        upd_id = int(input("Введите ID студента для обновления оценок: "))
        if upd_id < 0:
            raise DataValidationError("ID студента должно быть целым положительным числом")
        new_grades_str = input("Введите новые оценки через запятую: ")
        new_grades = [int(g.strip()) for g in new_grades_str.split(',') if g.strip()]
        
        processing.update_student_grades(students, upd_id, new_grades)
        print("Оценки успешно обновлены.")
    except ValueError:
        print("Ошибка ввода: ID и оценки должны быть целыми числами.")
    except StudentAppException as e:
        print(f"Ошибка: {e}")


def action_stats(students: List[Student]):
    """действие: показ статистики."""
    if not students:
        print("Список студентов пуст, статистика недоступна.")
        return
    
    stats = processing.get_group_statistics(students)
    print("\n--- Статистика по группе ---")
    print(f"Всего студентов: {stats['student_count']}")
    print(f"Общий средний балл: {stats['overall_average']:.2f}")
    print(f"Лучший студент: {stats['best_student'].name} (ср. балл: {stats['best_student'].average:.2f})")
    print(f"Худший студент: {stats['worst_student'].name} (ср. балл: {stats['worst_student'].average:.2f})")


def action_export_top(students: List[Student]):
    """действие: экспорт топ-n студентов."""
    if not students:
        print("Список студентов пуст. Нечего экспортировать.")
        return
    try:
        n = int(input("Введите количество студентов для экспорта (ТОП-N): "))
        if n <= 0:
            print("Ошибка: количество должно быть положительным числом.")
            return
        
        path = input("Введите путь для сохранения CSV файла (например: data/topn.csv: ").strip()
        if not path.lower().endswith('.csv'):
            print("Ошибка: файл должен иметь расширение .csv")
            return
        
        csv_data = processing.export_top_n_students_to_csv_string(students, n)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(csv_data)
        print(f"ТОП-{n} студентов успешно экспортированы в '{path}'")
    except ValueError:
        print("Ошибка ввода: количество должно быть целым числом.")
    except IOError as e:
        print(f"Ошибка записи в файл: {e}")


def action_sort(students: List[Student]):
    """действие: сортировка и показ студентов."""
    if not students:
        print("Список студентов пуст. Нечего сортировать.")
        return
    
    key = input("Введите ключ сортировки (id, name, avg): ").lower().strip()
    try:
        sorted_students = processing.sort_students(students, by=key)
        print(f"\n--- Студенты, отсортированные по '{key}' ---")
        show_students(sorted_students)
    except StudentAppException as e:
        print(f"Ошибка: {e}")


def main():
    """главный цикл работы консольного приложения."""
    students: List[Student] = []
    
    actions = {
        '1': action_load,
        '2': action_save,
        '3': lambda s: show_students(s),
        '4': action_add,
        '5': action_remove,
        '6': action_update,
        '7': action_stats,
        '8': action_export_top,
        '9': action_sort,
    }

    while True:
        print_menu()
        choice = input("Выберите пункт меню: ").strip()

        if choice == '0':
            print("Выход из программы.")
            sys.exit(0)
        
        action = actions.get(choice)
        
        if action:
            # для action_load нужно обновить список студентов
            if choice == '1':
                students = action(students)
            else:
                action(students)
        else:
            print("Неверный пункт меню. Пожалуйста, попробуйте снова.")
        
        press_enter_to_continue()


if __name__ == '__main__':
    main()