"""
Модуль для работы с внешними API (конвертация валют).
"""

import os
from typing import Any, Dict

import requests
from dotenv import load_dotenv

load_dotenv()


def convert_amount_to_rub(transaction: Dict[str, Any]) -> float:
    """
    Конвертирует сумму транзакции в рубли.

    Args:
        transaction: Словарь с данными о транзакции.

    Returns:
        Сумма в рублях (float).
    """
    try:
        amount = float(transaction.get('amount', 0.0))
        currency = transaction.get('currency', {}).get('code', 'RUB')

        if currency.upper() == 'RUB':
            return amount

        if currency.upper() in ('USD', 'EUR'):
            return _convert_via_api(amount, currency)

        return 0.0

    except (ValueError, TypeError, AttributeError):
        return 0.0


def _convert_via_api(amount: float, currency: str) -> float:
    """Конвертирует сумму через внешнее API."""
    api_key = os.getenv('EXCHANGE_API_KEY')
    if not api_key:
        return 0.0

    url = "https://api.apilayer.com/exchangerates_data/convert"
    headers = {"apikey": api_key}
    params = {
        "to": "RUB",
        "from": currency.upper(),
        "amount": amount
    }

    try:
        response = requests.get(url, headers=headers, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()

        if data.get('success'):
            return float(data.get('result', 0.0))
        return 0.0

    except (requests.RequestException, ValueError, KeyError):
        return 0.0
