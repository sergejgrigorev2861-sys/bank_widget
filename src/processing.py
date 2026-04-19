"""
Модуль для обработки данных банковских операций.
"""

from typing import List, Dict, Any


def filter_by_state(transactions: List[Dict[str, Any]], state: str = 'EXECUTED') -> List[Dict[str, Any]]:
    """
    Фильтрует список словарей по значению ключа 'state'.

    Args:
        transactions: Список словарей с данными транзакций
        state: Значение для фильтрации (по умолчанию 'EXECUTED')

    Returns:
        Новый список словарей с указанным значением state
    """
    return [item for item in transactions if item.get('state') == state]


def sort_by_date(transactions: List[Dict[str, Any]], descending: bool = True) -> List[Dict[str, Any]]:
    """
    Сортирует список словарей по дате (ключ 'date').

    Args:
        transactions: Список словарей с данными транзакций
        descending: Порядок сортировки (True - убывание, False - возрастание)

    Returns:
        Новый список, отсортированный по дате
    """
    return sorted(transactions, key=lambda x: x.get('date', ''), reverse=descending)
