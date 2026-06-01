"""
Модуль для чтения финансовых транзакций из CSV и Excel файлов.
"""

from pathlib import Path
from typing import Any, Dict, List

import pandas as pd


def read_csv_transactions(file_path: str) -> List[Dict[str, Any]]:
    """
    Считывает транзакции из CSV-файла и возвращает список словарей.

    Args:
        file_path: Путь к CSV-файлу

    Returns:
        Список словарей с транзакциями. При ошибке возвращает пустой список.
    """
    path = Path(file_path)

    if not path.exists():
        return []

    try:
        df = pd.read_csv(file_path)
        df = df.fillna(value=None)
        return df.to_dict(orient='records')
    except Exception:
        return []


def read_excel_transactions(file_path: str) -> List[Dict[str, Any]]:
    """
    Считывает транзакции из Excel-файла (XLSX) и возвращает список словарей.

    Args:
        file_path: Путь к Excel-файлу

    Returns:
        Список словарей с транзакциями. При ошибке возвращает пустой список.
    """
    path = Path(file_path)

    if not path.exists():
        return []

    try:
        df = pd.read_excel(file_path)
        df = df.fillna(value=None)
        return df.to_dict(orient='records')
    except Exception:
        return []
