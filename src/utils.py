"""
Модуль с утилитами для работы с транзакциями.
"""

import json
from pathlib import Path
from typing import Any, Dict, List


def load_transactions(file_path: str) -> List[Dict[str, Any]]:
    """
    Загружает транзакции из JSON-файла.

    Args:
        file_path: Путь до JSON-файла.

    Returns:
        Список словарей с данными о транзакциях.
        Если файл пустой, содержит не список, не найден или повреждён,
        возвращает пустой список.
    """
    path = Path(file_path)

    if not path.exists():
        return []

    if not path.is_file():
        return []

    try:
        with open(path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        if not isinstance(data, list):
            return []

        return data

    except (json.JSONDecodeError, OSError, IOError):
        return []
