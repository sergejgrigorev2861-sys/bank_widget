"""
Модуль для поиска транзакций по описанию с использованием регулярных выражений.
"""

import re
from typing import Any, Dict, List


def search_transactions(transactions: List[Dict[str, Any]], search_string: str) -> List[Dict[str, Any]]:
    """
    Ищет транзакции, содержащие заданную строку в поле 'description'.

    Args:
        transactions: Список словарей с транзакциями
        search_string: Строка для поиска

    Returns:
        Список транзакций, у которых description содержит search_string
    """
    if not transactions or not search_string:
        return []

    pattern = re.compile(re.escape(search_string), re.IGNORECASE)
    result = []

    for transaction in transactions:
        description = transaction.get('description', '')
        if pattern.search(str(description)):
            result.append(transaction)

    return result
