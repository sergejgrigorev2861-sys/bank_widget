from src.search_utils import search_transactions


def test_search_transactions_found():
    """Поиск существующего слова."""
    transactions = [
        {'description': 'Перевод организации'},
        {'description': 'Открытие вклада'},
        {'description': 'Перевод с карты на карту'},
    ]
    result = search_transactions(transactions, 'Перевод')
    assert len(result) == 2


def test_search_transactions_not_found():
    """Поиск отсутствующего слова."""
    transactions = [{'description': 'Открытие вклада'}]
    result = search_transactions(transactions, 'Покупка')
    assert result == []


def test_search_transactions_empty_list():
    """Пустой список транзакций."""
    result = search_transactions([], 'test')
    assert result == []


def test_search_transactions_empty_search_string():
    """Пустая строка поиска."""
    transactions = [{'description': 'test'}]
    result = search_transactions(transactions, '')
    assert result == []


def test_search_transactions_case_insensitive():
    """Регистронезависимый поиск."""
    transactions = [{'description': 'ПЕРЕВОД ОРГАНИЗАЦИИ'}]
    result = search_transactions(transactions, 'перевод')
    assert len(result) == 1
