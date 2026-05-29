"""
Модуль настройки логирования для проекта.
"""


import logging
from pathlib import Path


def setup_logger(name: str, log_file: str, level=logging.INFO) -> logging.Logger:
    """
    Настраивает и возвращает логгер для указанного модуля.

    Args:
         name: Имя логгера (обычно __name__)
         log_file: Имя файла лога (например, 'masks.log')
         level: Уровень логирования

    Returns:
          Настроенный логер
    """
    logs_dir = Path(__file__).parent.parent / "logs"
    logs_dir.mkdir(exist_ok=True)

    log_path = logs_dir / log_file

    logger = logging.getLogger(name)
    logger.setLevel(level)

    if logger.hasHandlers():
        logger.handlers.clear()

    file_handler = logging.FileHandler(log_path, mode='w', encoding='utf-8')
    file_handler.setLevel(level)

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    return logger
