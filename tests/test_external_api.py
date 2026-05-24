"""Тесты для модуля external_api."""

from unittest.mock import patch, Mock
from src.external_api import convert_amount_to_rub


def test_convert_rub_to_rub():
    """Конвертация рублей в рубли."""
    transaction = {"amount": "100.50", "currency": {"code": "RUB"}}
    assert convert_amount_to_rub(transaction) == 100.50


def test_convert_usd_to_rub_success():
    """Успешная конвертация USD в RUB."""
    transaction = {"amount": "100", "currency": {"code": "USD"}}
    mock_response = Mock()
    mock_response.json.return_value = {"success": True, "result": 9500.00}
    mock_response.raise_for_status = Mock()

    with patch('src.external_api.requests.get') as mock_get:
        mock_get.return_value = mock_response
        assert convert_amount_to_rub(transaction) == 9500.00


def test_convert_usd_to_rub_api_error():
    """Ошибка API."""
    transaction = {"amount": "100", "currency": {"code": "USD"}}
    with patch('src.external_api.requests.get', side_effect=Exception("API Error")):
        assert convert_amount_to_rub(transaction) == 0.0


def test_convert_unsupported_currency():
    """Неподдерживаемая валюта."""
    transaction = {"amount": "100", "currency": {"code": "GBP"}}
    assert convert_amount_to_rub(transaction) == 0.0


def test_convert_no_api_key():
    """Отсутствует API ключ."""
    transaction = {"amount": "100", "currency": {"code": "USD"}}
    with patch('src.external_api.os.getenv', return_value=None):
        with patch('src.external_api.requests.get') as mock_get:
            assert convert_amount_to_rub(transaction) == 0.0
            mock_get.assert_not_called()


def test_convert_invalid_amount():
    """Некорректная сумма."""
    transaction = {"amount": "not a number", "currency": {"code": "USD"}}
    with patch('src.external_api.requests.get') as mock_get:
        assert convert_amount_to_rub(transaction) == 0.0
        mock_get.assert_not_called()
