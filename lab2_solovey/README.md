# Команды
## Начальная инициализация
- `python3 -m venv .venv`
- `source .venv/bin/activate`
- `pip install -r requirements-dev.txt`
## Структуры проекта
- `mkdir -p lab`
    - `touch lab/__init__.py lab/main.py lab/models.py lab/processing.py lab/io_utils.py lab/errors.py`
- `mkdir -p data`
    - `touch data/students.csv`
- `mkdir -p tests`
    - `touch tests/__init__.py tests/conftest.py tests/test_models.py tests/test_processing.py tests/test_io_utils.py tests/test_main_cli.py`
    - `touch pytest.ini`
- `touch .gitignore README.md`