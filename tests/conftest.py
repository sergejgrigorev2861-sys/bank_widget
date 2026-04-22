import pytest


@pytest.fixture
def sample_transactions():
    """Фикстура с тестовыми данными для processing функций"""
    return [
        {"id": 1, "state": "EXECUTED", "date": "2024-01-03"},
        {"id": 2, "state": "EXECUTED", "date": "2024-01-01"},
        {"id": 3, "state": "CANCELED", "date": "2024-01-02"},
    ]
