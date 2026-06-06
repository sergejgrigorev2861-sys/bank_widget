"""
Модуль с утилитами для работы с транзакциями.
"""

import json
from pathlib import Path
from typing import Any, Dict, List

import pandas as pd

from src.logger_config import setup_logger

logger = setup_logger(__name__, 'utils.log')


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
    logger.info(f"Вызвана load_transactions с файлом: {file_path}")

    path = Path(file_path)

    if not path.exists():
        logger.warning(f"Файл не найден: {file_path}")
        return []

    if not path.is_file():
        logger.warning(f"Путь не является файлом: {file_path}")
        return []

    try:
        with open(path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        logger.info(f"Файл успешно прочитан: {file_path}")

        if not isinstance(data, list):
            logger.warning(f"Данные не список, а {type(data)}")
            return []

        logger.info(f"Загруженно {len(data)} транзакций")
        return data

    except (json.JSONDecodeError, OSError, IOError) as e:
        logger.error(f"Ошибка при загрузке файла {file_path}: {e}")
        return []


def load_transactions_from_excel(file_path: str) -> List[Dict[str, Any]]:
    """
    Загружает транзакции из Excel-файла.

    Args:
        file_path: Путь до Excel-файла.

    Returns:
        Список словарей с данными о транзакциях.
        При ошибке возвращает пустой список.
    """
    logger.info(f"Вызвана load_transactions_from_excel с файлом: {file_path}")

    path = Path(file_path)

    if not path.exists():
        logger.warning(f"Файл не найден: {file_path}")
        return []

    if not path.is_file():
        logger.warning(f"Путь не является файлом: {file_path}")
        return []

    try:
        df = pd.read_excel(file_path, dtype=str)
        df = df.where(pd.notnull(df), None)
        data = df.to_dict(orient='records')

        logger.info(f"Файл Excel успешно прочитан: {file_path}")
        logger.info(f"Загружено {len(data)} транзакций")
        return data

    except Exception as e:
        logger.error(f"Ошибка при загрузке Excel-файла {file_path}: {e}")
        return []
