import pytest
from lab.models import Student
from lab.io_utils import load_students_from_csv, save_students_to_csv
from lab.errors import DataValidationError


@pytest.fixture
def sample_students():
    return [
        Student(1, "Иванов Иван", [78, 85, 90]),
        Student(2, "Петров Петр", [65, 70]),  # разное количество оценок
        Student(3, "Сидорова Анна", [])      # без оценок
    ]


def test_load_students_with_header(tmp_path):
    """тест загрузки студентов из csv с заголовком."""
    csv_file = tmp_path / "students.csv"
    csv_content = (
        "id,name,grade1,grade2,grade3\n"
        "1,Иванов Иван,78,85,90\n"
        "2,Петров Петр,65,70,\n"  # пустая ячейка в конце
        "3,Сидорова Анна,,\n"     # пустые ячейки
        "\n"                      # пустая строка
    )
    csv_file.write_text(csv_content, encoding='utf-8')

    students = load_students_from_csv(str(csv_file), has_header=True)

    assert len(students) == 3
    assert students[0].id == 1
    assert students[0].name == "Иванов Иван"
    assert students[0].grades == [78, 85, 90]
    assert students[1].id == 2
    assert students[1].grades == [65, 70]
    assert students[2].id == 3
    assert students[2].grades == []


def test_load_students_no_header(tmp_path):
    """тест загрузки студентов из csv без заголовка."""
    csv_file = tmp_path / "students_no_header.csv"
    csv_content = (
        "1,Иванов Иван,100\n"
        "2,Петров Петр,88"
    )
    csv_file.write_text(csv_content, encoding='utf-8')

    students = load_students_from_csv(str(csv_file), has_header=False)

    assert len(students) == 2
    assert students[0].id == 1
    assert students[1].grades == [88]


def test_load_from_nonexistent_file():
    """тест на попытку загрузки из несуществующего файла."""
    with pytest.raises(FileNotFoundError):
        load_students_from_csv("nonexistent_file.csv", has_header=True)


def test_load_with_invalid_data(tmp_path):
    """тест на загрузку файла с некорректными данными."""
    csv_file = tmp_path / "invalid_data.csv"
    csv_content = "id,name\nnot_an_id,Имя"
    csv_file.write_text(csv_content, encoding='utf-8')

    with pytest.raises(DataValidationError) as excinfo:
        load_students_from_csv(str(csv_file), has_header=True)
    assert "ошибка в строке 2" in str(excinfo.value)


def test_save_students_and_roundtrip(tmp_path, sample_students):
    """
    сохраняем студентов в файл, а затем читаем
    и проверяем, что данные не исказились.
    """
    csv_file = tmp_path / "roundtrip.csv"

    # 1. сохраняем данные
    save_students_to_csv(str(csv_file), sample_students, include_header=True)

    # 2. читаем данные из только что созданного файла
    loaded_students = load_students_from_csv(str(csv_file), has_header=True)

    # 3. сравниваем исходные и загруженные данные
    assert len(loaded_students) == len(sample_students)
    for original, loaded in zip(sample_students, loaded_students):
        assert original.id == loaded.id
        assert original.name == loaded.name
        assert original.grades == loaded.grades


def test_save_students_column_alignment(tmp_path, sample_students):
    """
    тест на выравнивание колонок при сохранении.
    """
    csv_file = tmp_path / "aligned.csv"
    save_students_to_csv(str(csv_file), sample_students, include_header=True)

    content = csv_file.read_text(encoding='utf-8').strip().split('\n')
    
    # максимальное количество оценок у нас 3 (у Иванова)
    # значит, в каждой строке должно быть 2 (id, name) + 3 (grades) = 5 колонок
    # => 4 запятых
    
    # заголовок
    assert content[0] == "id,name,grade1,grade2,grade3"
    # у Петрова (2 оценки) должна быть одна пустая ячейка в конце
    assert content[2] == "2,Петров Петр,65,70,"
    # у Сидоровой (0 оценок) должно быть три пустых ячейки
    assert content[3] == "3,Сидорова Анна,,,"