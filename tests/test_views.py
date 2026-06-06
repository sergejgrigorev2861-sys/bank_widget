import json
from datetime import datetime
from unittest.mock import mock_open, patch

from src.views import (
    events_page,
    get_cards_info,
    get_currency_rates,
    get_date_range,
    get_greeting,
    get_stock_prices,
    get_top_transactions,
    main_page,
)


def test_get_date_range_month():
    start, end = get_date_range("2022-01-15", "M")
    assert start == datetime(2022, 1, 1)
    assert end == datetime(2022, 1, 15)


def test_get_date_range_week():
    start, end = get_date_range("2022-01-15", "W")
    # 15 января 2022 — суббота, начало недели понедельник 10 января
    assert start == datetime(2022, 1, 10)
    assert end == datetime(2022, 1, 15)


def test_get_date_range_year():
    start, end = get_date_range("2022-01-15", "Y")
    assert start == datetime(2022, 1, 1)
    assert end == datetime(2022, 1, 15)


def test_get_date_range_all():
    start, end = get_date_range("2022-01-15", "ALL")
    assert start == datetime(1970, 1, 1)
    assert end == datetime(2022, 1, 15)


def test_events_page_returns_json():
    result = events_page("2022-01-15", "M")
    assert result.startswith("{")
    assert "expenses" in result
    assert "income" in result


def test_get_currency_rates():
    with patch('builtins.open', mock_open(read_data=json.dumps({
        "user_currencies": ["USD", "EUR"]
    }))):
        with patch('requests.get') as mock_get:
            mock_get.return_value.json.return_value = {
                "rates": {"RUB": 73.46}
            }
            rates = get_currency_rates()
            assert len(rates) == 2
            assert rates[0]["currency"] == "USD"
            assert "rate" in rates[0]


def test_get_stock_prices():
    with patch('builtins.open', mock_open(read_data=json.dumps({
        "user_stocks": ["AAPL", "GOOGL"]
    }))):
        with patch('yfinance.Ticker') as MockTicker:
            mock_ticker = MockTicker.return_value
            mock_ticker.history.return_value.empty = False
            mock_ticker.history.return_value['Close'].iloc[-1] = 150.12
            prices = get_stock_prices()
            assert len(prices) == 2
            assert prices[0]["stock"] == "AAPL"
            assert "price" in prices[0]


def test_events_page_with_test_excel():

    result_json = events_page("2021-12-31", "M")
    data = json.loads(result_json)
    assert "expenses" in data
    assert "income" in data
    assert data["expenses"]["total_amount"] > 0


def test_events_page_period_week():

    result = events_page("2021-12-31", "W")
    data = json.loads(result)
    assert "expenses" in data
    assert "income" in data
    assert data["expenses"]["total_amount"] > 0


def test_events_page_period_year():

    result = events_page("2021-12-31", "Y")
    data = json.loads(result)
    assert "expenses" in data
    assert "income" in data
    assert data["expenses"]["total_amount"] > 0


def test_events_page_period_all():

    result = events_page("2022-01-15", "ALL")
    data = json.loads(result)
    assert "expenses" in data
    assert "income" in data
    assert data["expenses"]["total_amount"] > 0


def test_events_page_no_data():

    with patch('src.views.load_transactions_from_excel', return_value=[]):
        result = events_page("2022-01-15", "M")
        assert "error" in json.loads(result)


def test_events_page_invalid_date():

    with patch('src.views.load_transactions_from_excel', return_value=[]):
        result = events_page("invalid", "M")
        # Должен вернуть ошибку, так как дата не парсится
        assert "expenses" not in json.loads(result)


def test_get_currency_rates_file_not_found():

    with patch('builtins.open', side_effect=FileNotFoundError):
        rates = get_currency_rates()
        assert rates == []


def test_get_currency_rates_api_error():

    with patch('builtins.open', mock_open(read_data=json.dumps({"user_currencies": ["USD"]}))):
        with patch('requests.get', side_effect=Exception("API Error")):
            rates = get_currency_rates()
            assert rates == []


def test_get_currency_rates_empty_response():

    with patch('builtins.open', mock_open(read_data=json.dumps({"user_currencies": ["USD"]}))):
        with patch('requests.get') as mock_get:
            mock_get.return_value.json.return_value = {}
            rates = get_currency_rates()
            assert rates == []


def test_get_stock_prices_file_not_found():

    with patch('builtins.open', side_effect=FileNotFoundError):
        prices = get_stock_prices()
        assert prices == []


def test_get_stock_prices_yfinance_error():

    with patch('builtins.open', mock_open(read_data=json.dumps({"user_stocks": ["AAPL"]}))):
        with patch('yfinance.Ticker', side_effect=Exception("YFinance error")):
            prices = get_stock_prices()
            assert len(prices) == 1
            assert prices[0]["stock"] == "AAPL"
            assert prices[0]["price"] is None


def test_events_page_invalid_period():

    with patch('src.views.load_transactions_from_excel', return_value=[]):
        result = events_page("2022-01-15", "INVALID")
        # Должен вернуть ошибку (или обработать как 'M')
        assert isinstance(json.loads(result), dict)


def test_events_page_invalid_date_format():

    # Данные с неправильным форматом даты
    invalid_data = [
        {"Дата операции": "31-12-2021", "Категория": "Супермаркеты", "Сумма операции": -100}
    ]

    with patch('src.views.load_transactions_from_excel', return_value=invalid_data):
        result = events_page("2021-12-31", "M")
        data = json.loads(result)
        # Должен быть пустой результат, так как дата не распарсилась
        assert data["expenses"]["total_amount"] == 0


def test_events_page_missing_date():

    missing_date_data = [
        {"Категория": "Супермаркеты", "Сумма операции": -100}
    ]

    with patch('src.views.load_transactions_from_excel', return_value=missing_date_data):
        result = events_page("2021-12-31", "M")
        data = json.loads(result)
        assert data["expenses"]["total_amount"] == 0


def test_events_page_invalid_amount():

    invalid_amount_data = [
        {"Дата операции": "31.12.2021 00:00:00", "Категория": "Супермаркеты", "Сумма операции": "abc"}
    ]

    with patch('src.views.load_transactions_from_excel', return_value=invalid_amount_data):
        result = events_page("2021-12-31", "M")
        data = json.loads(result)
        # Некорректная сумма не должна попасть в расходы
        assert len(data["expenses"]["main"]) == 0


def test_events_page_no_category():

    no_category_data = [
        {"Дата операции": "31.12.2021 00:00:00", "Сумма операции": -100}
    ]

    with patch('src.views.load_transactions_from_excel', return_value=no_category_data):
        result = events_page("2021-12-31", "M")
        data = json.loads(result)
        # Должна появиться категория "Без категории"
        categories = [item["category"] for item in data["expenses"]["main"]]
        assert "Без категории" in categories


def test_events_page_empty_expenses():

    # Все транзакции — доходы
    income_only = [
        {"Дата операции": "31.12.2021 00:00:00", "Категория": "Зарплата", "Сумма операции": 1000}
    ]

    with patch('src.views.load_transactions_from_excel', return_value=income_only):
        result = events_page("2021-12-31", "M")
        data = json.loads(result)
        assert data["expenses"]["main"] == []
        assert data["expenses"]["transfers_and_cash"] == []
        assert data["income"]["main"] != []


def test_events_page_advanced():

    periods = [
        ("M", "2021-12-31"),
        ("W", "2021-12-31"),
        ("Y", "2021-12-31"),
        ("ALL", "2022-01-15"),
    ]
    for period, date in periods:
        result = events_page(date, period)
        data = json.loads(result)
        assert "expenses" in data
        assert "income" in data
        assert data["expenses"]["total_amount"] > 0


def test_get_currency_rates_empty_currencies():

    with patch('builtins.open', mock_open(read_data=json.dumps({"user_currencies": []}))):
        rates = get_currency_rates()
        assert rates == []


def test_events_page_other_sum():

    data = json.loads(events_page("2021-12-31", "M"))
    main_cats = data["expenses"]["main"]
    if any(cat["category"] == "Остальное" for cat in main_cats):
        assert main_cats[-1]["category"] == "Остальное"


def test_events_page_load_error():

    with patch('src.views.load_transactions_from_excel', return_value=[]):
        result = events_page("2021-12-31", "M")
        data = json.loads(result)
        assert "error" in data


def test_get_currency_rates_full_coverage():

    settings = {"user_currencies": ["USD", "EUR"]}
    with patch('builtins.open', mock_open(read_data=json.dumps(settings))):
        with patch('requests.get') as mock_get:
            # Создаём объект ответа с методом json()
            mock_response = mock_get.return_value
            mock_response.json.return_value = {"rates": {"RUB": 73.46}}
            rates = get_currency_rates()
            assert len(rates) == 2


def test_get_greeting_morning():
    with patch('src.views.datetime') as mock_datetime:
        mock_datetime.now.return_value.hour = 8
        assert get_greeting() == "Доброе утро"


def test_get_greeting_afternoon():
    with patch('src.views.datetime') as mock_datetime:
        mock_datetime.now.return_value.hour = 14
        assert get_greeting() == "Добрый день"


def test_get_greeting_evening():
    with patch('src.views.datetime') as mock_datetime:
        mock_datetime.now.return_value.hour = 20
        assert get_greeting() == "Добрый вечер"


def test_get_greeting_night():
    with patch('src.views.datetime') as mock_datetime:
        mock_datetime.now.return_value.hour = 3
        assert get_greeting() == "Доброй ночи"


def test_main_page():

    with patch('src.views.load_transactions_from_excel', return_value=[{"id": 1}]):  # не пусто
        with patch('src.views.get_cards_info',
                   return_value=[{"last_digits": "1234", "total_spent": 100, "cashback": 1}]):
            with patch('src.views.get_top_transactions',
                       return_value=[{"date": "01.01.2020", "amount": 100, "category": "cat", "description": "desc"}]):
                with patch('src.views.get_currency_rates', return_value=[{"currency": "USD", "rate": 70.0}]):
                    with patch('src.views.get_stock_prices', return_value=[{"stock": "AAPL", "price": 150.0}]):
                        result = main_page("2025-06-06 15:30:00")
                        data = json.loads(result)
                        assert "greeting" in data
                        assert "cards" in data
                        assert "top_transactions" in data
                        assert "currency_rates" in data
                        assert "stock_prices" in data


def test_main_page_with_real_data():

    # Тестовые транзакции
    test_transactions = [
        {"Номер карты": "*7197", "Сумма операции": -100.0, "Категория": "Еда",
            "Описание": "Магазин", "Дата операции": "2021-12-31"},
        {"Номер карты": "*5091",
         "Сумма операции": -50.0,
         "Категория": "Транспорт",
         "Описание": "Такси",
         "Дата операции": "2021-12-30"},
    ]

    with patch('src.views.load_transactions_from_excel', return_value=test_transactions):
        with patch('src.views.get_currency_rates', return_value=[]):
            with patch('src.views.get_stock_prices', return_value=[]):
                result = main_page("2025-06-06 15:30:00")
                data = json.loads(result)
                assert "cards" in data
                assert len(data["cards"]) > 0
                assert "top_transactions" in data
                assert len(data["top_transactions"]) > 0


def test_get_date_range_unknown_period():

    start, end = get_date_range("2022-01-15", "X")
    # По логике, неизвестный период должен обрабатываться как месяц (с 1 числа)
    assert start == datetime(2022, 1, 1)
    assert end == datetime(2022, 1, 15)


def test_get_cards_info_short_card():

    transactions = [
        {"Номер карты": "123", "Сумма операции": -100}  # всего 3 цифры
    ]
    result = get_cards_info(transactions)
    assert result == []  # такие карты должны игнорироваться


def test_get_cards_info_invalid_amount():

    transactions = [
        {"Номер карты": "*1234", "Сумма операции": "abc"}  # не число
    ]
    result = get_cards_info(transactions)
    assert result == []  # такие транзакции не должны добавляться


def test_get_top_transactions_invalid_date():

    transactions = [
        {"Дата операции": "31.12.2021", "Сумма операции": 100, "Категория": "cat", "Описание": "desc"}
    ]
    result = get_top_transactions(transactions)
    # Дата должна остаться как есть (без преобразования)
    assert result[0]["date"] == "31.12.2021"


def test_get_currency_rates_no_rub():

    settings = {"user_currencies": ["USD"]}
    with patch('builtins.open', mock_open(read_data=json.dumps(settings))):
        with patch('requests.get') as mock_get:
            mock_get.return_value.json.return_value = {"rates": {}}  # нет RUB
            rates = get_currency_rates()
            assert rates == []  # курс не получен


def test_get_stock_prices_empty_data():

    settings = {"user_stocks": ["AAPL"]}
    with patch('builtins.open', mock_open(read_data=json.dumps(settings))):
        with patch('yfinance.Ticker') as MockTicker:
            mock_ticker = MockTicker.return_value
            mock_ticker.history.return_value.empty = True
            prices = get_stock_prices()
            assert prices[0]["price"] is None


def test_main_page_no_data():

    with patch('src.views.load_transactions_from_excel', return_value=[]):
        result = main_page("2025-06-06 15:30:00")
        data = json.loads(result)
        assert "error" in data


def test_get_stock_prices_exception():

    settings = {"user_stocks": ["AAPL"]}
    with patch('builtins.open', mock_open(read_data=json.dumps(settings))):
        with patch('yfinance.Ticker', side_effect=Exception("API error")):
            prices = get_stock_prices()
            assert prices[0]["price"] is None


def test_get_cards_info_none_card():

    transactions = [
        {"Номер карты": None, "Сумма операции": -100},
        {"Номер карты": "None", "Сумма операции": -200}
    ]
    result = get_cards_info(transactions)
    assert result == []  # такие карты игнорируются


def test_get_currency_rates_generic_exception():

    with patch('builtins.open', side_effect=PermissionError("Access denied")):
        rates = get_currency_rates()
        assert rates == []


def test_get_stock_prices_file_exception():

    with patch('builtins.open', side_effect=PermissionError("Access denied")):
        prices = get_stock_prices()
        assert prices == []


def test_get_stock_prices_empty_stocks():

    settings = {"user_stocks": []}
    with patch('builtins.open', mock_open(read_data=json.dumps(settings))):
        prices = get_stock_prices()
        assert prices == []
