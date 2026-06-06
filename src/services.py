import json
import logging
import re
from typing import Any, Dict, List

from src.utils import load_transactions_from_excel

logger = logging.getLogger(__name__)


def search_transactions(transactions: List[Dict[str, Any]], query: str) -> List[Dict[str, Any]]:
    """
    Ищет транзакции, где в поле 'Описание' или 'Категория' встречается query (регистронезависимо).

    Аргументы:
        transactions: список транзакций
        query: строка поиска

    Возвращает:
        отфильтрованный список транзакций
    """
    if not query:
        return []

    query_lower = query.lower()
    result = []

    for t in transactions:
        description = str(t.get("Описание", "")).lower()
        category = str(t.get("Категория", "")).lower()

        if query_lower in description or query_lower in category:
            result.append(t)

    logger.info(f"Поиск по '{query}' нашёл {len(result)} транзакций")
    return result


def main_search(query: str) -> str:
    """
    Загружает транзакции из Excel и возвращает JSON с результатами поиска.
    """
    transactions = load_transactions_from_excel('data/operations.xlsx')
    if not transactions:
        logger.error("Не удалось загрузить транзакции")
        return json.dumps({"error": "Не удалось загрузить данные"})

    filtered = search_transactions(transactions, query)

    return json.dumps(filtered, ensure_ascii=False, indent=2, default=str)


def search_phone_numbers(transactions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Возвращает транзакции, в описании которых встречается номер телефона.
    Поддерживаются форматы: +7 xxx xxx-xx-xx, 8 xxx xxx-xx-xx, +7 (xxx) xxx-xx-xx и т.п.
    """
    # Регулярное выражение для поиска телефонных номеров (Россия)
    # Группа: +7 или 8, затем разделители, затем 10 цифр
    phone_pattern = re.compile(
        r'(\+7|8)[\s\-\(]*(\d{3})[\s\-\)]*(\d{3})[\s\-]*(\d{2})[\s\-]*(\d{2})'
    )

    result = []
    for t in transactions:
        description = str(t.get("Описание", ""))
        if phone_pattern.search(description):
            result.append(t)
            logger.info(f"Найден телефон в транзакции: {description[:50]}...")
    return result


def main_phone_search() -> str:
    """
    Загружает транзакции и возвращает JSON с транзакциями, где есть телефон.
    """
    transactions = load_transactions_from_excel('data/operations.xlsx')
    if not transactions:
        return json.dumps({"error": "Не удалось загрузить данные"})

    filtered = search_phone_numbers(transactions)
    return json.dumps(filtered, ensure_ascii=False, indent=2, default=str)


def top_cashback_categories(transactions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Возвращает топ-3 категории с наибольшим кешбэком.
    """
    cashback_by_category = {}
    for t in transactions:
        category = t.get("Категория")
        cashback_str = t.get("Кэшбэк")
        if not category or not cashback_str:
            continue
        try:
            cashback = float(cashback_str)
        except (ValueError, TypeError):
            continue
        cashback_by_category[category] = cashback_by_category.get(category, 0.0) + cashback

    sorted_cats = sorted(cashback_by_category.items(), key=lambda x: x[1], reverse=True)
    return [{"category": cat, "cashback": round(cb, 2)} for cat, cb in sorted_cats[:3]]
