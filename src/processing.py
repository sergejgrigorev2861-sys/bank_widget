import re
from collections import Counter
from typing import Any, Dict, List


def filter_by_state(transactions: List[Dict[str, Any]], state: str = 'EXECUTED') -> List[Dict[str, Any]]:
    return [item for item in transactions if item.get('state') == state]


def sort_by_date(transactions: List[Dict[str, Any]], descending: bool = True) -> List[Dict[str, Any]]:
    return sorted(transactions, key=lambda x: x.get('date', ''), reverse=descending)


def count_operations_by_category(transactions: List[Dict[str, Any]], categories: List[str]) -> Dict[str, int]:
    """
    Подсчитывает количество операций в каждой категории на основе поля description.

    Args:
        transactions: Список словарей с транзакциями
        categories: Список категорий для подсчёта

    Returns:
        Словарь {категория: количество}
    """
    if not transactions or not categories:
        return {category: 0 for category in categories}

    counter = Counter()

    for transaction in transactions:
        description = transaction.get('description', '')
        for category in categories:
            if re.search(re.escape(category), description, re.IGNORECASE):
                counter[category] += 1
                break  # Одна транзакция попадает только в одну категорию

    return dict(counter)
