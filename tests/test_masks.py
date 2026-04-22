import pytest
from src.masks import get_mask_card_number, get_mask_account


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