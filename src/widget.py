"""
Модуль для маскировки банковских карт и счетов,
а так же для форматирования дат из ISO-формата
"""

from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(info: str) -> str:
    """
    Принимает строку с типом и номером карты/счета.
    Возвращает строку с замаскированным номером.
    """
    parts = info.rsplit(' ', 1)
    if len(parts) != 2:
        return info

    name_part = parts[0]
    number_part = parts[1]

    if name_part.lower() == "счет":
        masked_number = get_mask_account(int(number_part))
    else:
        masked_number = get_mask_card_number(int(number_part))

    return f"{name_part} {masked_number}"


def get_date(date_string: str) -> str:
    """
    Принимает дату в формате "2024-03-11T02:26:18.671407"
    Возвращает дату в формате "ДД.ММ.ГГГГ"
    """
    date_part = date_string.split('T')[0]
    year, month, day = date_part.split('-')
    return f"{day}.{month}.{year}"
