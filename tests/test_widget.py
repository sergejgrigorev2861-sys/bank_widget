import pytest

from src.widget import get_date, mask_account_card


@pytest.mark.parametrize("input_data, expected", [
    ("Visa Platinum 7000792289606361", "Visa Platinum 7000 79** **** 6361"),
    ("Счет 73654108430135874305", "Счет **4305"),
    ("MasterCard 1234567890123456", "MasterCard 1234 56** **** 3456"),
])
def test_mask_account_card(input_data, expected):
    assert mask_account_card(input_data) == expected


@pytest.mark.parametrize("date_str, expected", [
    ("2024-03-11T12:30:45", "11.03.2024"),
    ("2023-12-01T00:00:00", "01.12.2023"),
    ("2024-01-01T23:59:59", "01.01.2024"),
])
def test_get_date(date_str, expected):
    assert get_date(date_str) == expected


def test_mask_account_card_invalid():
    assert mask_account_card("") == ""
