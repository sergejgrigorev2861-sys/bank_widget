"""
Модуль для маскировки номеров карт и счетов.
"""


from src.logger_config import setup_logger

logger = setup_logger(__name__, 'masks.log')


def get_mask_card_number(card_number: int) -> str:
    """
    Принимает номер карты (число из 16 цифр) и возвращает маску вида:
    XXXX XX** **** XXXX
    """
    logger.info(f"Вызвана get_mask_card_number с аргументом: {card_number}")

    card_str = str(card_number)

    if len(card_str) != 16:
        logger.error(f"Некорректная длина номера карты: {len(card_str)} (ожидается 16)")
        return "Неверный номер карты"

    first_six = card_str[:6]
    last_four = card_str[-4:]

    result = f"{first_six[:4]} {first_six[4:6]}** **** {last_four}"
    logger.info(f"Успешно замаскирован номер карты: {result}")
    return result


def get_mask_account(account_number: int) -> str:
    """
    Принимает номер счета (число) и возвращает маску вида:
    **XXXX (видны только последние 4 цифры)
    """
    logger.info(f"Вызвана get_mask_account с аргументом: {account_number}")

    account_str = str(account_number)

    if len(account_str) < 4:
        logger.error(f"Номер счета слишком короткий: {len(account_str)} (минимум 4 цифры)")
        return "Неверный номер счета"

    result = f"**{account_str[-4:]}"
    logger.info(f"Успешно замаскирован номер счета: {result}")
    return result
