"""
Модуль для маскировки банковских карт и счетов,
а так же для форматирования дат из ISO-формата
"""

from src.masks import get_mask_card_number, get_mask_account


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


# Тесты для проверки (можно запустить файл, чтобы убедиться, что всё работает)
if __name__ == "__main__":
    test_cases = [
        "Maestro 1596837868705199",
        "Счет 64686473678894779589",
        "MasterCard 7158300734726758",
        "Visa Platinum 8990922113665229",
        "Счет 73654108430135874305",
    ]
    print("=== Тестирование mask_account_card ===")
    for case in test_cases:
        print(f"{case} -> {mask_account_card(case)}")

    print("\n=== Тестирование get_date ===")
    test_date = "2024-03-11T02:26:18.671407"
    print(f"{test_date} -> {get_date(test_date)}")