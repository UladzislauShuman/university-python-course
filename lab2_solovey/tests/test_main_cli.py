import pytest
from lab import main


def test_main_cli_scenario(monkeypatch, capsys, tmp_path):
    """
    тестирует базовый сценарий работы cli:
    """
    # создаем временный csv-файл с одним студентом
    test_file = tmp_path / "test_students.csv"
    user_inputs = [
        '3',  # 1. показать всех (список должен быть пуст)
        '1',  # 2. загрузить из csv
        str(test_file),  # путь к нашему временному файлу
        'n',  # файл без заголовка
        '3',  # 3. снова показать всех (теперь должен быть 1 студент)
        '7',  # 4. показать статистику
        '0'   # 5. выйти из программы
    ]
    test_file.write_text("1,Тестов Тест,100", encoding='utf-8')
    
    input_generator = iter(user_inputs)
    
    monkeypatch.setattr('builtins.input', lambda _: next(input_generator))

    main.main_loop()

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