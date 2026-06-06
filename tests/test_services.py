import pytest
from src.services import search_transactions

def test_search_transactions_found():
    data = [
        {"Описание": "Перевод другу", "Категория": "Переводы"},
        {"Описание": "Покупка в магазине", "Категория": "Супермаркеты"}
    ]
    result = search_transactions(data, "перевод")
    assert len(result) == 1
    assert result[0]["Описание"] == "Перевод другу"

def test_search_transactions_not_found():
    data = [{"Описание": "Покупка", "Категория": "Супермаркеты"}]
    result = search_transactions(data, "перевод")
    assert result == []

def test_search_transactions_empty_query():
    data = [{"Описание": "Перевод"}]
    result = search_transactions(data, "")
    assert result == []

def test_search_phone_numbers():
    from src.services import search_phone_numbers

    data = [
        {"Описание": "Перевод +7 921 123-45-67"},
        {"Описание": "Покупка в магазине"},
        {"Описание": "Звонок 8 981 234-56-78"},
        {"Описание": "Перевод без телефона"}
    ]
    result = search_phone_numbers(data)
    assert len(result) == 2
    assert "+7 921 123-45-67" in result[0]["Описание"]
    assert "8 981 234-56-78" in result[1]["Описание"]

def test_search_phone_numbers_no_phones():
    from src.services import search_phone_numbers

    data = [
        {"Описание": "Обычная транзакция"},
        {"Описание": "Покупка"}
    ]
    result = search_phone_numbers(data)
    assert result == []

def test_top_cashback_categories():
    from src.services import top_cashback_categories

    transactions = [
        {"Категория": "Супермаркеты", "Кэшбэк": "10.5"},
        {"Категория": "Супермаркеты", "Кэшбэк": "5.2"},
        {"Категория": "Аптеки", "Кэшбэк": "20.0"},
        {"Категория": "Аптеки", "Кэшбэк": "15.0"},
        {"Категория": "Кафе", "Кэшбэк": "8.0"},
        {"Категория": "Такси", "Кэшбэк": "3.0"},
    ]
    result = top_cashback_categories(transactions)
    # Ожидаем топ-3: Аптеки (35.0), Супермаркеты (15.7), Кафе (8.0)
    assert len(result) == 3
    assert result[0]["category"] == "Аптеки"
    assert result[0]["cashback"] == 35.0
    assert result[1]["category"] == "Супермаркеты"
    assert result[1]["cashback"] == 15.7
    assert result[2]["category"] == "Кафе"
    assert result[2]["cashback"] == 8.0


def test_top_cashback_categories_empty():
    from src.services import top_cashback_categories

    assert top_cashback_categories([]) == []


def test_top_cashback_categories_no_cashback():
    from src.services import top_cashback_categories

    transactions = [
        {"Категория": "Супермаркеты", "Кэшбэк": None},
        {"Категория": "Аптеки", "Кэшбэк": ""},
        {"Категория": "Кафе", "Кэшбэк": "abc"},
    ]
    result = top_cashback_categories(transactions)
    assert result == []  # нет валидного кешбэка


def test_top_cashback_categories_less_than_three():
    from src.services import top_cashback_categories

    transactions = [
        {"Категория": "Супермаркеты", "Кэшбэк": "10.0"},
        {"Категория": "Аптеки", "Кэшбэк": "5.0"},
    ]
    result = top_cashback_categories(transactions)
    assert len(result) == 2
    assert result[0]["category"] == "Супермаркеты"
    assert result[1]["category"] == "Аптеки"

def test_main_search_load_error():
    from src.services import main_search
    from unittest.mock import patch
    import json

    with patch('src.services.load_transactions_from_excel', return_value=[]):
        result = main_search("перевод")
        data = json.loads(result)
        assert "error" in data


def test_main_search_success():
    from src.services import main_search
    from unittest.mock import patch
    import json

    test_transactions = [{"Описание": "Перевод другу", "Категория": "Переводы"}]
    with patch('src.services.load_transactions_from_excel', return_value=test_transactions):
        result = main_search("перевод")
        data = json.loads(result)
        assert len(data) == 1
        assert data[0]["Описание"] == "Перевод другу"

def test_main_phone_search_load_error():
    from src.services import main_phone_search
    from unittest.mock import patch
    import json

    with patch('src.services.load_transactions_from_excel', return_value=[]):
        result = main_phone_search()
        data = json.loads(result)
        assert "error" in data


def test_main_phone_search_success():
    from src.services import main_phone_search
    from unittest.mock import patch
    import json

    test_transactions = [{"Описание": "Мой телефон +7 921 123-45-67"}]
    with patch('src.services.load_transactions_from_excel', return_value=test_transactions):
        with patch('src.services.search_phone_numbers', return_value=test_transactions):
            result = main_phone_search()
            data = json.loads(result)
            assert len(data) == 1
            assert "+7 921 123-45-67" in data[0]["Описание"]

