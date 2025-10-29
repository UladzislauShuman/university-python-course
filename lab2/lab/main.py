"""
главный модуль приложения.

содержит консольный интерфейс пользователя (cli) для управления
списком студентов. является точкой входа в программу.
"""

from typing import List

# импортируем все необходимые компоненты из нашего пакета
from .models import Student
from lab.io_utils import load_students_from_csv, save_students_to_csv
from lab.processing import get_group_statistics, export_top_n_students_to_csv_string, sort_students
from lab.errors import DuplicateStudentIdError, StudentNotFoundError, DataValidationError, StudentAppException

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


def main_loop():
    """главный цикл работы консольного приложения."""
    students: List[Student] = []

    while True:
        print_menu()
        choice = input("Выберите пункт меню: ").strip()

        try:
            # --- 1. Загрузка из CSV ---
            if choice == '1':
                filepath = input("Введите путь к файлу для загрузки: ")
                has_header = input("Файл содержит заголовок? (y/n): ").lower() == 'y'
                students = load_students_from_csv(filepath, has_header)
                print(f"Успешно загружено {len(students)} студентов.")

            # --- 2. Сохранение в CSV ---
            elif choice == '2':
                if not students:
                    print("Список студентов пуст. Нечего сохранять.")
                    continue
                filepath = input("Введите путь к файлу для сохранения: ")
                include_header = input("Включить заголовок в файл? (y/n): ").lower() == 'y'
                save_students_to_csv(filepath, students, include_header)
                print(f"Данные успешно сохранены в {filepath}")

            # --- 3. Показ всех студентов ---
            elif choice == '3':
                if not students:
                    print("Список студентов пуст.")
                else:
                    print("\n--- Список студентов ---")
                    for s in students:
                        print(s)

            # --- 4. Добавление студента ---
            elif choice == '4':
                try:
                    new_id = int(input("Введите ID нового студента: "))
                    # проверяем, не занят ли уже этот id
                    if any(s.id == new_id for s in students):
                        raise DuplicateStudentIdError(f"Студент с ID {new_id} уже существует.")
                    
                    name = input("Введите ФИО студента: ")
                    grades_str = input("Введите оценки через запятую (например, 80,95,78): ")
                    grades = [int(g.strip()) for g in grades_str.split(',') if g.strip()]
                    
                    new_student = Student(id=new_id, name=name, grades=grades)
                    students.append(new_student)
                    print(f"Студент '{name}' успешно добавлен.")
                except ValueError:
                    print("Ошибка: ID и оценки должны быть числами.")
                except DataValidationError as e:
                    print(f"Ошибка валидации: {e}")

            # --- 5. Удаление студента ---
            elif choice == '5':
                try:
                    del_id = int(input("Введите ID студента для удаления: "))
                    student_to_delete = next((s for s in students if s.id == del_id), None)
                    if student_to_delete:
                        students.remove(student_to_delete)
                        print(f"Студент с ID {del_id} успешно удален.")
                    else:
                        raise StudentNotFoundError(f"Студент с ID {del_id} не найден.")
                except ValueError:
                    print("Ошибка: ID должен быть числом.")

            # --- 6. Обновление оценок ---
            elif choice == '6':
                try:
                    upd_id = int(input("Введите ID студента для обновления оценок: "))
                    student_to_update = next((s for s in students if s.id == upd_id), None)
                    if student_to_update:
                        print(f"Текущие оценки студента '{student_to_update.name}': {student_to_update.grades}")
                        new_grades_str = input("Введите новые оценки через запятую: ")
                        new_grades = [int(g.strip()) for g in new_grades_str.split(',') if g.strip()]
                        # валидируем оценки перед присвоением
                        for grade in new_grades:
                            if not (0 <= grade <= 100):
                                raise DataValidationError("Оценки должны быть в диапазоне от 0 до 100.")
                        student_to_update.grades = new_grades
                        print("Оценки успешно обновлены.")
                    else:
                        raise StudentNotFoundError(f"Студент с ID {upd_id} не найден.")
                except ValueError:
                    print("Ошибка: ID и оценки должны быть числами.")
                except DataValidationError as e:
                    print(f"Ошибка валидации: {e}")

            # --- 7. Статистика ---
            elif choice == '7':
                stats = get_group_statistics(students)
                if stats["student_count"] == 0:
                    print("Список студентов пуст, статистика недоступна.")
                else:
                    print("\n--- Статистика по группе ---")
                    print(f"Всего студентов: {stats['student_count']}")
                    print(f"Общий средний балл: {stats['overall_average']:.2f}")
                    print(f"Лучший студент: {stats['best_student'].name} (ср. балл: {stats['best_student'].average:.2f})")
                    print(f"Худший студент: {stats['worst_student'].name} (ср. балл: {stats['worst_student'].average:.2f})")

            # --- 8. Экспорт ТОП-N ---
            elif choice == '8':
                try:
                    n = int(input("Введите количество студентов для экспорта (ТОП-N): "))
                    if n <= 0:
                        print("Количество должно быть положительным числом.")
                        continue
                    
                    # получаем csv-строку от нашей processing функции
                    csv_data = export_top_n_students_to_csv_string(students, n)
                    
                    filepath = input("Введите путь к файлу для сохранения экспорта: ")
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(csv_data)
                    print(f"ТОП-{n} студентов успешно экспортированы в {filepath}")
                except ValueError:
                    print("Ошибка: количество должно быть числом.")

            # --- 9. Сортировка ---
            elif choice == '9':
                sort_key = input("Введите ключ сортировки (id, name, avg): ").lower().strip()
                if sort_key not in ['id', 'name', 'avg']:
                    print("Неверный ключ сортировки. Доступные ключи: id, name, avg.")
                    continue
                
                sorted_students = sort_students(students, sort_key)
                print(f"\n--- Студенты, отсортированные по '{sort_key}' ---")
                for s in sorted_students:
                    print(s)

            # --- 0. Выход ---
            elif choice == '0':
                print("Выход из программы.")
                break

            # --- Неверный ввод ---
            else:
                print("Неверный пункт меню. Пожалуйста, попробуйте снова.")

        # --- Глобальный обработчик ошибок ---
        # ловим наши кастомные ошибки
        except StudentAppException as e:
            print(f"Ошибка приложения: {e}")
        # ловим ошибки файловой системы
        except (FileNotFoundError, PermissionError, IOError) as e:
            print(f"Ошибка работы с файлом: {e}")
        # ловим все остальные непредвиденные ошибки
        except Exception as e:
            print(f"Произошла непредвиденная ошибка: {e}")


if __name__ == '__main__':
    main_loop()