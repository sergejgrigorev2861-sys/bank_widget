"""
Модуль с генераторами для обработки транзакций.
"""

from typing import Any, Dict, Iterator, List


def filter_by_currency(transactions: List[Dict[str, Any]], currency: str) -> Iterator[Dict[str, Any]]:
    """
    Фильтрует транзакции по заданной валюте.
    """
    for transaction in transactions:
        try:
            if transaction.get("operationAmount", {}).get("currency", {}).get("code") == currency:
                yield transaction
        except (AttributeError, TypeError, KeyError):
            continue


def transaction_descriptions(transactions: List[Dict[str, Any]]) -> Iterator[str]:
    """
    Генерирует описания транзакций по очереди.
    """
    for transaction in transactions:
        try:
            description = transaction.get("description", "")
            if description:
                yield description
        except (AttributeError, TypeError):
            continue


def card_number_generator(start: int, stop: int) -> Iterator[str]:
    """
    Генерирует номера банковских карт в заданном диапазоне.
    """
    if start < 1 or stop > 9999999999999999:
        raise ValueError("Номер карты должен быть в диапазоне от 1 до 9999999999999999")
    if start > stop:
        raise ValueError("start не может быть больше stop")

    for number in range(start, stop + 1):
        formatted = f"{number:016d}"
        yield f"{formatted[:4]} {formatted[4:8]} {formatted[8:12]} {formatted[12:16]}"
