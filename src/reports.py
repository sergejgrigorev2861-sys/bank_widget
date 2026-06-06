import json
import logging
from datetime import datetime
from typing import Optional, List, Dict, Any
import pandas as pd
from src.utils import load_transactions_from_excel

logger = logging.getLogger(__name__)


def report_decorator(filename: Optional[str] = None):
    """
    Декоратор для отчётов: сохраняет результат функции в JSON-файл.
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            output_filename = filename if filename else f"{func.__name__}.json"
            with open(output_filename, 'w', encoding='utf-8') as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
            return result
        return wrapper
    return decorator


@report_decorator()
def spending_by_category(category: str, date: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Возвращает траты по заданной категории за последние 3 месяца от даты.
    """
    transactions = load_transactions_from_excel('data/operations.xlsx')
    if not transactions:
        return []

    # Если дата не указана — берём текущую
    if date is None:
        end_date = datetime.now()
    else:
        end_date = datetime.strptime(date, '%Y-%m-%d')

    # Вычисляем дату 3 месяца назад
    start_date = end_date - pd.DateOffset(months=3)

    filtered = []
    for t in transactions:
        # Берём дату операции и преобразуем из формата DD.MM.YYYY HH:MM:SS
        date_str = t.get("Дата операции")
        if not date_str or not isinstance(date_str, str):
            continue
        try:
            # Отделяем дату от времени (до пробела)
            date_part = date_str.split()[0] # "31.12.2021"
            t_date = datetime.strptime(date_part, '%d.%m.%Y')
        except (ValueError, TypeError):
            continue

        # Проверяем категорию и диапазон дат
        if t.get("Категория") == category and start_date <= t_date <= end_date:
            filtered.append(t)

    return filtered
