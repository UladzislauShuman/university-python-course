"""
тесты для консольного интерфейса в main.py.
"""
import pytest
from lab import main


def test_main_cli_scenario(monkeypatch, capsys, tmp_path):
    """
    тестирует базовый сценарий работы cli:
    1. показать пустой список.
    2. загрузить данные из файла.
    3. показать загруженных студентов.
    4. показать статистику.
    5. выйти.
    """
    # --- подготовка ---
    test_file = tmp_path / "test_students.csv"
    test_file.write_text("1,Тестов Тест,100", encoding='utf-8')

    user_inputs = [
        '3',              # 1. показать всех (список должен быть пуст)
        "",               # Enter
        '1',              # 2. загрузить из csv
        str(test_file),   # путь к нашему временному файлу
        'n',              # файл без заголовка
        "",               # Enter
        '3',              # 3. снова показать всех (теперь должен быть 1 студент)
        "",               # Enter
        '7',              # 4. показать статистику
        "",               # Enter
        '0'               # 5. выйти из программы
    ]
    
    input_generator = iter(user_inputs)
    monkeypatch.setattr('builtins.input', lambda _: next(input_generator))

    # --- действие и проверка ---
    with pytest.raises(SystemExit) as e:
        main.main()
    
    # проверяем, что программа завершилась с кодом 0
    assert e.value.code == 0

    # проверяем, что было выведено в консоль
    captured_output = capsys.readouterr().out
    
    # 1
    assert "Список студентов пуст." in captured_output
    
    # 2
    assert "Успешно загружено 1 студентов." in captured_output
    
    # 3
    assert "ID: 1, Имя: Тестов Тест, Оценки: [100], Средний балл: 100.00" in captured_output
    
    # 4
    assert "Всего студентов: 1" in captured_output
    assert "Лучший студент: Тестов Тест" in captured_output
    
    # 5
    assert "Выход из программы." in captured_output