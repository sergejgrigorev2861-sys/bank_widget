"""
Модуль для маскировки номеров карт и счетов.
"""


def get_mask_card_number(card_number: int) -> str:
    """
    Принимает номер карты (число из 16 цифр) и возвращает маску вида:
    XXXX XX** **** XXXX
    """
    card_str = str(card_number)
    first_six = card_str[:6]
    last_four = card_str[-4:]
    return f"{first_six[:4]} {first_six[4:6]}** **** {last_four}"


def get_mask_account(account_number: int) -> str:
    """
    Принимает номер счета (число) и возвращает маску вида:
    **XXXX (видны только последние 4 цифры)
    """
    account_str = str(account_number)
    return f"**{account_str[-4:]}"
