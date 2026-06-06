"""Тесты для модуля utils."""

import json
from unittest.mock import mock_open, patch

import pytest

from src.utils import load_transactions


@pytest.fixture
def temp_json_file(tmp_path):
    """Создаёт временный JSON-файл для тестов."""
    def _create_file(data, filename="operations.json"):
        file_path = tmp_path / filename
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f)
        return str(file_path)
    return _create_file


def test_load_transactions_success(temp_json_file):
    """Тест: успешная загрузка транзакций."""
    test_data = [
        {"id": 1, "amount": 100, "currency": {"code": "RUB"}},
        {"id": 2, "amount": 200, "currency": {"code": "USD"}}
    ]
    file_path = temp_json_file(test_data)
    result = load_transactions(file_path)
    assert result == test_data


def test_load_transactions_empty_list(temp_json_file):
    """Тест: пустой список."""
    file_path = temp_json_file([])
    result = load_transactions(file_path)
    assert result == []


def test_load_transactions_not_a_list(temp_json_file):
    """Тест: файл содержит не список."""
    file_path = temp_json_file({"key": "value"})
    result = load_transactions(file_path)
    assert result == []


def test_load_transactions_file_not_found():
    """Тест: файл не найден."""
    with patch('pathlib.Path.exists', return_value=False):
        result = load_transactions("nonexistent.json")
        assert result == []


def test_load_transactions_not_a_file():
    """Тест: путь указывает на директорию, а не на файл."""
    with patch('pathlib.Path.exists', return_value=True):
        with patch('pathlib.Path.is_file', return_value=False):
            result = load_transactions("/some/directory")
            assert result == []


def test_load_transactions_invalid_json(tmp_path):
    """Тест: повреждённый JSON."""
    file_path = tmp_path / "bad.json"
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write("{invalid json}")
    result = load_transactions(str(file_path))
    assert result == []


def test_load_transactions_json_decode_error():
    """Тест: ошибка JSONDecodeError."""
    with patch('pathlib.Path.exists', return_value=True):
        with patch('pathlib.Path.is_file', return_value=True):
            with patch('builtins.open', mock_open(read_data="invalid json")):
                with patch('json.load', side_effect=json.JSONDecodeError("Expecting value", "doc", 0)):
                    result = load_transactions("/any/path.json")
                    assert result == []


def test_load_transactions_os_error():
    """Тест: ошибка OSError (покрывает except)."""
    with patch('pathlib.Path.exists', return_value=True):
        with patch('pathlib.Path.is_file', return_value=True):
            with patch('builtins.open', side_effect=OSError("Permission denied")):
                result = load_transactions("/any/path.json")
                assert result == []


def test_load_transactions_io_error():
    """Тест: ошибка IOError (покрывает except)."""
    with patch('pathlib.Path.exists', return_value=True):
        with patch('pathlib.Path.is_file', return_value=True):
            with patch('builtins.open', side_effect=IOError("Input/output error")):
                result = load_transactions("/any/path.json")
                assert result == []

def test_load_transactions_from_excel_file_not_found():
    from src.utils import load_transactions_from_excel
    from unittest.mock import patch

    with patch('pathlib.Path.exists', return_value=False):
        result = load_transactions_from_excel("nonexistent.xlsx")
        assert result == []


def test_load_transactions_from_excel_not_a_file():
    from src.utils import load_transactions_from_excel
    from unittest.mock import patch

    with patch('pathlib.Path.exists', return_value=True):
        with patch('pathlib.Path.is_file', return_value=False):
            result = load_transactions_from_excel("some_directory")
            assert result == []


def test_load_transactions_from_excel_exception():
    from src.utils import load_transactions_from_excel
    from unittest.mock import patch

    with patch('pathlib.Path.exists', return_value=True):
        with patch('pathlib.Path.is_file', return_value=True):
            with patch('pandas.read_excel', side_effect=Exception("Read error")):
                result = load_transactions_from_excel("bad.xlsx")
                assert result == []
