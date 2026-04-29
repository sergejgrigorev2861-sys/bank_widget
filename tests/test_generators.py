"""
Тесты для модуля generators.
"""

import pytest
from src.generators import filter_by_currency, transaction_descriptions, card_number_generator


@pytest.fixture
def sample_transactions():
    """Возвращает список тестовых транзакций."""
    return [
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {
                "amount": "9824.07",
                "currency": {"name": "USD", "code": "USD"}
            },
            "description": "Перевод организации",
        },
        {
            "id": 142264268,
            "state": "EXECUTED",
            "date": "2019-04-04T23:20:05.206878",
            "operationAmount": {
                "amount": "79114.93",
                "currency": {"name": "USD", "code": "USD"}
            },
            "description": "Перевод со счета на счет",
        },
        {
            "id": 873106923,
            "state": "EXECUTED",
            "date": "2019-03-23T01:09:46.296404",
            "operationAmount": {
                "amount": "43318.34",
                "currency": {"name": "руб.", "code": "RUB"}
            },
            "description": "Перевод со счета на счет",
        },
        {
            "id": 895315941,
            "state": "EXECUTED",
            "date": "2018-08-19T04:27:37.904916",
            "operationAmount": {
                "amount": "56883.54",
                "currency": {"name": "USD", "code": "USD"}
            },
            "description": "Перевод с карты на карту",
        },
    ]


class TestFilterByCurrency:
    def test_filter_usd_returns_correct_transactions(self, sample_transactions):
        """Проверяет, что фильтрация по USD возвращает только USD-транзакции."""
        usd_filter = filter_by_currency(sample_transactions, "USD")
        result = list(usd_filter)
        assert len(result) == 3
        for trans in result:
            assert trans["operationAmount"]["currency"]["code"] == "USD"

    def test_filter_rub_returns_correct_transactions(self, sample_transactions):
        """Проверяет, что фильтрация по RUB возвращает только RUB-транзакции."""
        rub_filter = filter_by_currency(sample_transactions, "RUB")
        result = list(rub_filter)
        assert len(result) == 1
        assert result[0]["operationAmount"]["currency"]["code"] == "RUB"

    def test_filter_nonexistent_currency_returns_empty(self, sample_transactions):
        """Проверяет, что фильтрация по несуществующей валюте возвращает пустой результат."""
        eur_filter = filter_by_currency(sample_transactions, "EUR")
        result = list(eur_filter)
        assert result == []

    def test_filter_empty_list_returns_empty(self):
        """Проверяет, что фильтрация пустого списка не вызывает ошибку."""
        empty_filter = filter_by_currency([], "USD")
        result = list(empty_filter)
        assert result == []


class TestFilterByCurrencyErrors:
    def test_filter_by_currency_handles_attribute_error(self):
        """Проверяет, что генератор обрабатывает AttributeError."""
        transactions = [None]
        gen = filter_by_currency(transactions, "USD")
        result = list(gen)
        assert result == []

    def test_filter_by_currency_handles_type_error(self):
        """Проверяет, что генератор обрабатывает TypeError."""
        transactions = [123]
        gen = filter_by_currency(transactions, "USD")
        result = list(gen)
        assert result == []

    def test_filter_by_currency_handles_key_error(self):
        """Проверяет, что генератор обрабатывает KeyError."""
        transactions = [{"id": 1}]
        gen = filter_by_currency(transactions, "USD")
        result = list(gen)
        assert result == []


class TestTransactionDescriptions:
    def test_returns_correct_descriptions(self, sample_transactions):
        """Проверяет, что функция возвращает корректные описания."""
        descriptions = list(transaction_descriptions(sample_transactions))
        expected = [
            "Перевод организации",
            "Перевод со счета на счет",
            "Перевод со счета на счет",
            "Перевод с карты на карту",
        ]
        assert descriptions == expected

    def test_empty_list_returns_empty(self):
        """Проверяет, что для пустого списка возвращается пустой результат."""
        result = list(transaction_descriptions([]))
        assert result == []


class TestTransactionDescriptionsErrors:
    def test_transaction_descriptions_handles_attribute_error(self):
        """Проверяет, что генератор обрабатывает AttributeError."""
        transactions = [None]
        gen = transaction_descriptions(transactions)
        result = list(gen)
        assert result == []

    def test_transaction_descriptions_handles_type_error(self):
        """Проверяет, что генератор обрабатывает TypeError."""
        transactions = [123]
        gen = transaction_descriptions(transactions)
        result = list(gen)
        assert result == []

    def test_transaction_descriptions_skips_empty_description(self):
        """Проверяет, что генератор пропускает пустые описания."""
        transactions = [{"description": ""}]
        gen = transaction_descriptions(transactions)
        result = list(gen)
        assert result == []


class TestCardNumberGenerator:
    @pytest.mark.parametrize("start,stop,expected", [
        (1, 1, ["0000 0000 0000 0001"]),
        (1, 5, [
            "0000 0000 0000 0001",
            "0000 0000 0000 0002",
            "0000 0000 0000 0003",
            "0000 0000 0000 0004",
            "0000 0000 0000 0005",
        ]),
        (9999, 9999, ["0000 0000 0000 9999"]),
    ])
    def test_generates_correct_numbers(self, start, stop, expected):
        """Проверяет генерацию номеров карт в разных диапазонах."""
        result = list(card_number_generator(start, stop))
        assert result == expected

    def test_start_greater_than_stop_raises_error(self):
        """Проверяет, что при start > stop выбрасывается исключение."""
        with pytest.raises(ValueError, match="start не может быть больше stop"):
            list(card_number_generator(10, 5))

    def test_start_less_than_1_raises_error(self):
        """Проверяет, что при start < 1 выбрасывается исключение."""
        with pytest.raises(ValueError, match="Номер карты должен быть в диапазоне от 1 до 9999999999999999"):
            list(card_number_generator(0, 10))

    def test_stop_greater_than_max_raises_error(self):
        """Проверяет, что при stop > 9999999999999999 выбрасывается исключение."""
        with pytest.raises(ValueError, match="Номер карты должен быть в диапазоне от 1 до 9999999999999999"):
            list(card_number_generator(1, 10000000000000000))