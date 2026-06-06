import pytest
from src.reports import spending_by_category

def test_spending_by_category_with_date():
    # Можно передать реальные данные из Excel или использовать заглушку
    # Для простоты пока тест на структуру
    result = spending_by_category("Супермаркеты", "2022-01-15")
    assert isinstance(result, list)

def test_spending_by_category_no_date():
    result = spending_by_category("Супермаркеты")
    assert isinstance(result, list)

def test_spending_by_category_file_not_found():
    from src.reports import spending_by_category
    from unittest.mock import patch

    with patch('src.reports.load_transactions_from_excel', return_value=[]):
        result = spending_by_category("Супермаркеты", "2022-01-15")
        assert result == []


def test_spending_by_category_invalid_date():
    from src.reports import spending_by_category
    from unittest.mock import patch
    import pandas as pd

    # Данные с неправильным форматом даты
    invalid_data = [{"Дата операции": "31-12-2021", "Категория": "Супермаркеты"}]
    with patch('src.reports.load_transactions_from_excel', return_value=invalid_data):
        with patch('pandas.DateOffset', return_value=pd.DateOffset(months=3)):
            result = spending_by_category("Супермаркеты", "2022-01-15")
            # Дата не распарсилась, транзакция не должна попасть в результат
            assert result == []


def test_spending_by_category_missing_date_field():
    from src.reports import spending_by_category
    from unittest.mock import patch

    missing_date = [{"Категория": "Супермаркеты"}]  # нет поля "Дата операции"
    with patch('src.reports.load_transactions_from_excel', return_value=missing_date):
        result = spending_by_category("Супермаркеты", "2022-01-15")
        assert result == []