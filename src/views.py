import json
import logging
from datetime import datetime, timedelta
from typing import Any, Dict, List

import requests
import yfinance as yf

from src.utils import load_transactions_from_excel

logger = logging.getLogger(__name__)


def get_date_range(date_str: str, period: str = 'M'):
    """
    Определяет начальную и конечную дату для анализа в зависимости от периода.
    period:
      'W' — неделя (включая дату)
      'M' — месяц (с начала месяца до даты)
      'Y' — год (с начала года до даты)
      'ALL' — все данные до даты (с 1970 года)
    """
    current = datetime.strptime(date_str, '%Y-%m-%d')
    end_date = current

    if period == 'W':
        # Начало недели (понедельник)
        start_date = current - timedelta(days=current.weekday())
    elif period == 'M':
        start_date = current.replace(day=1)
    elif period == 'Y':
        start_date = current.replace(month=1, day=1)
    elif period == 'ALL':
        start_date = datetime(1970, 1, 1)
    else:
        start_date = current.replace(day=1)

    return start_date, end_date


def get_greeting() -> str:
    """
    Возвращает приветствие в зависимости от текущего времени суток.
    """
    hour = datetime.now().hour

    if 6 <= hour < 12:
        return "Доброе утро"
    elif 12 <= hour < 18:
        return "Добрый день"
    elif 18 <= hour < 23:
        return "Добрый вечер"
    else:
        return "Доброй ночи"


def main_page(date_time_str: str) -> str:
    """
    Главная страница. Принимает дату/время в формате 'YYYY-MM-DD HH:MM:SS'.
    Возвращает JSON-строку с данными для веб-страницы.
    """
    greeting = get_greeting()

    # Загружаем транзакции
    transactions = load_transactions_from_excel('data/operations.xlsx')
    if not transactions:
        logger.error("Не удалось загрузить транзакции")
        return json.dumps({"error": "Не удалось загрузить данные"}, ensure_ascii=False, indent=2)

    # Пока просто напечатаем количество транзакций в лог
    logger.info(f"Загружено {len(transactions)} транзакций для главной страницы")

    # Получаем данные по картам
    cards_info = get_cards_info(transactions)

    top_transactions = get_top_transactions(transactions)

    currency_rates = get_currency_rates()

    stock_prices = get_stock_prices()

    result = {
        "greeting": greeting,
        "cards": cards_info,
        "top_transactions": top_transactions,
        "currency_rates": currency_rates,
        "stock_prices": stock_prices
    }

    return json.dumps(result, ensure_ascii=False, indent=2)


def get_cards_info(transactions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Принимает список транзакций, возвращает список словарей с данными по картам:
    - последние 4 цифры
    - общая сумма расходов
    - кешбэк (1 рубль на каждые 100 рублей расходов)
    """
    cards_data = {}

    for t in transactions:
        # Извлекаем номер карты из поля "Номер карты"
        card_num = t.get("Номер карты")
        if not card_num or card_num == "None":
            continue

        # Извлекаем только последние 4 цифры (очищаем от *)
        card_str = str(card_num)
        if len(card_str) >= 4:
            last_digits = card_str[-4:]
        else:
            continue

        # Сумма расхода (отрицательные значения — траты)
        amount_str = t.get("Сумма операции", 0)
        try:
            amount = float(amount_str)
        except (ValueError, TypeError):
            amount = 0.0

        # Учитываем только расходы (отрицательные суммы)
        if amount < 0:
            spent = abs(amount)
            if last_digits not in cards_data:
                cards_data[last_digits] = 0.0
            cards_data[last_digits] += spent

    # Формируем результат
    result = []
    for last_digits, total_spent in cards_data.items():
        cashback = round(total_spent / 100, 2)
        result.append({
            "last_digits": last_digits,
            "total_spent": round(total_spent, 2),
            "cashback": cashback
        })

    return result


def get_top_transactions(transactions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    # Сортируем транзакции по убыванию абсолютной суммы
    sorted_trans = sorted(
        transactions,
        key=lambda x: abs(float(x.get("Сумма операции", 0))),
        reverse=True
    )
    top5 = sorted_trans[:5]

    result = []
    for t in top5:
        # Преобразуем дату из формата YYYY-MM-DD в DD.MM.YYYY
        date_str = t.get("Дата операции", "")
        if isinstance(date_str, str) and "-" in date_str:
            parts = date_str.split("-")
            formatted_date = f"{parts[2]}.{parts[1]}.{parts[0]}" if len(parts) == 3 else date_str
        else:
            formatted_date = str(date_str)

        # Сумма как float
        amount = float(t.get("Сумма операции", 0))

        result.append({
            "date": formatted_date,
            "amount": amount,
            "category": t.get("Категория", ""),
            "description": t.get("Описание", "")
        })
    return result


def get_currency_rates() -> List[Dict[str, Any]]:
    print("DEBUG: get_currency_rates called")
    try:
        with open('user_settings.json', 'r', encoding='utf-8') as f:
            settings = json.load(f)
    except FileNotFoundError:
        logger.error("Файл user_settings.json не найден")
        return []
    except Exception as e:
        logger.error(f"Ошибка чтения user_settings.json: {e}")
        return []

    currencies = settings.get("user_currencies", [])
    if not currencies:
        return []

    rates = []
    for cur in currencies:
        # Пример API (бесплатный, без ключа)
        print(f"DEBUG: processing {cur}")
        url = f"https://api.exchangerate-api.com/v4/latest/{cur}"
        try:
            resp = requests.get(url, timeout=5)
            data = resp.json()
            rate = data.get("rates", {}).get("RUB")
            if rate:
                rates.append({"currency": cur, "rate": round(rate, 2)})
        except Exception as e:
            logger.error(f"Ошибка получения курса для {cur}: {e}")
    return rates


def get_stock_prices() -> List[Dict[str, Any]]:
    try:
        with open('user_settings.json', 'r', encoding='utf-8') as f:
            settings = json.load(f)
    except FileNotFoundError:
        logger.error("Файл user_settings.json не найден")
        return []
    except Exception as e:
        logger.error(f"Ошибка чтения user_settings.json: {e}")
        return []

    stocks = settings.get("user_stocks", [])
    if not stocks:
        return []

    prices = []
    for stock in stocks:
        try:
            ticker = yf.Ticker(stock)
            # Получаем текущую цену (последнее доступное значение)
            # history(period="1d") даст данные за сегодняшний день
            data = ticker.history(period="1d")
            if not data.empty:
                # 'Close' — цена закрытия, последняя цена за день
                price = round(float(data['Close'].iloc[-1]), 2)
                prices.append({"stock": stock, "price": price})
            else:
                logger.warning(f"Нет данных для {stock}")
                prices.append({"stock": stock, "price": None})
        except Exception as e:
            logger.error(f"Ошибка получения цены для {stock}: {e}")
            prices.append({"stock": stock, "price": None})
    return prices


def events_page(date_str: str, period: str = 'M') -> str:
    """
    Возвращает JSON с расходами, доходами, курсами валют и ценами акций за указанный период.
    """
    transactions = load_transactions_from_excel('data/operations.xlsx')
    if not transactions:
        return json.dumps({"error": "Не удалось загрузить данные"})

    start_date, end_date = get_date_range(date_str, period)

    # Фильтруем транзакции по дате
    filtered = []
    for t in transactions:
        date_str = t.get("Дата операции")
        if not date_str:
            continue
        try:
            date_part = date_str.split()[0]
            t_date = datetime.strptime(date_part, '%d.%m.%Y')
        except (ValueError, TypeError):
            continue
        if start_date <= t_date <= end_date:
            filtered.append(t)

    # Разделяем на расходы и доходы
    expenses = []
    incomes = []
    for t in filtered:
        amount_str = t.get("Сумма операции", "0")
        try:
            amount = float(amount_str)
        except (ValueError, TypeError):
            continue
        if amount < 0:
            expenses.append(t)
        else:
            incomes.append(t)

    # Группируем расходы по категориям
    expenses_by_category = {}
    for t in expenses:
        cat = t.get("Категория", "Без категории")
        amount = abs(float(t.get("Сумма операции", 0)))
        expenses_by_category[cat] = expenses_by_category.get(cat, 0) + amount

    # ... то же для доходов
    income_by_category = {}
    for t in incomes:
        cat = t.get("Категория", "Без категории")
        amount = float(t.get("Сумма операции", 0))
        income_by_category[cat] = income_by_category.get(cat, 0) + amount

    # Формируем результат
    result = {
        "expenses": {
            "total_amount": round(sum(expenses_by_category.values())),
            "main": [],
            "transfers_and_cash": []
        },
        "income": {
            "total_amount": round(sum(income_by_category.values())),
            "main": []
        },
        "currency_rates": get_currency_rates(),
        "stock_prices": get_stock_prices()
    }

    # Сортируем категории расходов по убыванию и берём топ-7
    sorted_expenses = sorted(expenses_by_category.items(), key=lambda x: x[1], reverse=True)
    main_cats = sorted_expenses[:7]
    other_sum = sum(v for _, v in sorted_expenses[7:])

    for cat, amt in main_cats:
        result["expenses"]["main"].append({"category": cat, "amount": round(amt)})
    if other_sum > 0:
        result["expenses"]["main"].append({"category": "Остальное", "amount": round(other_sum)})

    # Отдельно переводы и наличные
    transfers_and_cash = []
    for cat, amt in expenses_by_category.items():
        if cat in ["Переводы", "Наличные"]:
            transfers_and_cash.append({"category": cat, "amount": round(amt)})
    result["expenses"]["transfers_and_cash"] = sorted(transfers_and_cash, key=lambda x: x["amount"], reverse=True)

    # Удаляем из main категории, которые уже попали в transfers_and_cash
    result["expenses"]["main"] = [
        item for item in result["expenses"]["main"]
        if item["category"] not in ["Переводы", "Наличные"]
    ]

    # Топ доходов (все категории, без ограничения)
    sorted_incomes = sorted(income_by_category.items(), key=lambda x: x[1], reverse=True)
    for cat, amt in sorted_incomes:
        result["income"]["main"].append({"category": cat, "amount": round(amt)})

    return json.dumps(result, ensure_ascii=False, indent=2)
