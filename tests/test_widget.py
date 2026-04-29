"""
Тесты для модуля widget.
"""

import pytest
from src.widget import mask_account_card, get_date


class TestMaskAccountCard:
    @pytest.mark.parametrize("input_data,expected", [
        # Карты
        ("Maestro 1596837868705199", "Maestro 1596 83** **** 5199"),
        ("MasterCard 7158300734726758", "MasterCard 7158 30** **** 6758"),
        ("Visa Platinum 8990922113665229", "Visa Platinum 8990 92** **** 5229"),
        ("Visa Classic 1234567812345678", "Visa Classic 1234 56** **** 5678"),
        # Счета
        ("Счет 64686473678894779589", "Счет **9589"),
        ("Счет 73654108430135874305", "Счет **4305"),
    ])
    def test_mask_account_card_valid(self, input_data, expected):
        """Проверяет маскирование карт и счетов."""
        assert mask_account_card(input_data) == expected

    def test_mask_account_card_invalid_format(self):
        """Проверяет обработку некорректного формата (не разделяется на 2 части)."""
        assert mask_account_card("НеправильныйФормат") == "НеправильныйФормат"

    def test_mask_account_card_empty_string(self):
        """Проверяет обработку пустой строки."""
        assert mask_account_card("") == ""


class TestGetDate:
    @pytest.mark.parametrize("input_date,expected", [
        ("2024-03-11T02:26:18.671407", "11.03.2024"),
        ("2024-01-15T10:30:00", "15.01.2024"),
        ("2023-12-01T00:00:00", "01.12.2023"),
        ("2024-12-31T23:59:59", "31.12.2024"),
        ("2024-01-01T00:00:00", "01.01.2024"),
    ])
    def test_get_date_valid(self, input_date, expected):
        """Проверяет преобразование даты из ISO-формата."""
        assert get_date(input_date) == expected

    def test_get_date_without_time(self):
        """Проверяет дату без временной части."""
        assert get_date("2024-01-15") == "15.01.2024"

    def test_get_date_empty_string(self):
        """Проверяет обработку пустой строки."""
        with pytest.raises(ValueError):
            get_date("")
