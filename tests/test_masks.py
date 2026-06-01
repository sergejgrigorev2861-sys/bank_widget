import pytest

from src.masks import get_mask_account, get_mask_card_number


# Параметризация для get_mask_card_number
@pytest.mark.parametrize("card_number, expected", [
    (7000792289606361, "7000 79** **** 6361"),
    (1234567890123456, "1234 56** **** 3456"),
    (1111222233334444, "1111 22** **** 4444"),
    (0, "0 ** **** 0"),  # граничный случай
])
def test_get_mask_card_number(card_number, expected):
    assert get_mask_card_number(card_number) == expected


# Параметризация для get_mask_account
@pytest.mark.parametrize("account_number, expected", [
    (73654108430135874305, "**4305"),
    (12345678901234567890, "**7890"),
    (0, "**0"),
])
def test_get_mask_account(account_number, expected):
    assert get_mask_account(account_number) == expected


def test_get_mask_card_number_invalid_length():
    """Некорректная длина номера карты (не 16 и не 0)."""
    result = get_mask_card_number(12345)  # 5 цифр, не 16
    assert result == "Неверный номер карты"


def test_get_mask_account_invalid_length():
    """Некорректная длина номера счёта (меньше 4 цифр, не 0)."""
    result = get_mask_account(123)  # 3 цифры
    assert result == "Неверный номер счета"
