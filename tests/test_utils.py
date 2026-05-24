"""Тесты для модуля utils."""

import json
import pytest
from unittest.mock import patch
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


def test_load_transactions_invalid_json(tmp_path):
    """Тест: повреждённый JSON."""
    file_path = tmp_path / "bad.json"
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write("{invalid json}")
    result = load_transactions(str(file_path))
    assert result == []
