"""
Тесты для модуля processing.
"""

import pytest
from src.processing import filter_by_state, sort_by_date


@pytest.fixture
def sample_data():
    """Фикстура с тестовыми данными."""
    return [
        {"id": 1, "state": "EXECUTED", "date": "2024-01-15T10:00:00"},
        {"id": 2, "state": "CANCELED", "date": "2024-01-10T10:00:00"},
        {"id": 3, "state": "EXECUTED", "date": "2024-01-20T10:00:00"},
        {"id": 4, "state": "CANCELED", "date": "2024-01-05T10:00:00"},
    ]


class TestFilterByState:
    @pytest.mark.parametrize("state,expected_count", [
        ("EXECUTED", 2),
        ("CANCELED", 2),
        ("PENDING", 0),
    ])
    def test_filter_by_state(self, sample_data, state, expected_count):
        """Проверяет фильтрацию по разным статусам."""
        result = filter_by_state(sample_data, state)
        assert len(result) == expected_count
        if expected_count > 0:
            assert all(item["state"] == state for item in result)

    def test_filter_by_state_empty(self):
        """Проверяет обработку пустого списка."""
        assert filter_by_state([]) == []


class TestSortByDate:
    def test_sort_by_date_descending(self, sample_data):
        """Проверяет сортировку по дате по убыванию."""
        result = sort_by_date(sample_data)
        dates = [item["date"] for item in result]
        assert dates == ["2024-01-20T10:00:00", "2024-01-15T10:00:00", "2024-01-10T10:00:00", "2024-01-05T10:00:00"]

    def test_sort_by_date_empty(self):
        """Проверяет обработку пустого списка."""
        assert sort_by_date([]) == []

    def test_sort_by_date_same_dates(self):
        """Проверяет сортировку при одинаковых датах."""
        data = [
            {"id": 1, "date": "2024-01-15T10:00:00"},
            {"id": 2, "date": "2024-01-15T10:00:00"},
        ]
        result = sort_by_date(data)
        assert len(result) == 2