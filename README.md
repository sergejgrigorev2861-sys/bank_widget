# Bank Widget

Виджет для обработки банковских операций клиента.

## Цель проекта

Обеспечить удобную обработку данных о банковских операциях.

## Установка

```
git clone git@github.com:sergejgrigorev2861-sys/bank_widget.git
cd bank_widget
```

## Использование

```
from src.processing import filter_by_state, sort_by_date

transactions = [
    {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
    {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
    {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
]

# Фильтрация
executed = filter_by_state(transactions)
canceled = filter_by_state(transactions, 'CANCELED')

# Сортировка
sorted_by_date = sort_by_date(transactions)
```
## Модуль generators

Модуль содержит функции-генераторы для эффективной обработки больших объемов данных транзакций.

### Функции

#### `filter_by_currency(transactions, currency)`

Генератор, фильтрующий транзакции по заданной валюте.

```
from src.generators import filter_by_currency

usd_transactions = filter_by_currency(transactions, "USD")
first_usd = next(usd_transactions)
```

#### `transaction_descriptions(transactions)`
Генератор, возвращающий описания транзакций по очереди.

```
from src.generators import transaction_descriptions

descriptions = transaction_descriptions(transactions)
for desc in descriptions:
    print(desc)
```

#### `card_number_generator(start, stop)`
Генератор номеров банковских карт в заданном диапазоне.

```
from src.generators import card_number_generator

for card in card_number_generator(1, 5):
    print(card)
# 0000 0000 0000 0001
# 0000 0000 0000 0002
# 0000 0000 0000 0003
# 0000 0000 0000 0004
# 0000 0000 0000 0005
```

## Тестирование

```
pytest tests/
```

## Для проверки покрытия

```
pytest --cov=src --cov-report=html tests/
```

### Результаты тестирования

- Всего тестов: 19
- Покрытие кода: 100%

## Модуль decorators

### Декоратор `log`

Декоратор для логирования вызовов функций. Логирует результат выполнения или ошибку.

#### Параметры:
- `filename` (опционально) — имя файла для записи логов. Если не указан, логи выводятся в консоль.

#### Формат логов:
- При успехе: `имя_функции ok`
- При ошибке: `имя_функции error: тип_ошибки. Inputs: (args), {kwargs}`

#### Пример использования:

```python
from src.decorators import log

# Логирование в консоль
@log()
def add(a, b):
    return a + b

# Логирование в файл
@log(filename="logs.txt")
def divide(a, b):
    return a / b
```
## Модуль utils

### Функция `load_transactions(file_path)`

Загружает финансовые транзакции из JSON-файла.

```python
from src.utils import load_transactions

transactions = load_transactions("data/operations.json")
print(len(transactions))  # количество транзакций
```
Возвращает: список словарей с транзакциями или пустой список при ошибке.

Модуль external_api
Функция convert_amount_to_rub(transaction)
Конвертирует сумму транзакции из USD или EUR в рубли.

```python
from src.external_api import convert_amount_to_rub

transaction = {"amount": "100", "currency": {"code": "USD"}}
rub_amount = convert_amount_to_rub(transaction)  # 9500.0
```
Возвращает: float — сумму в рублях или 0.0 при ошибке.

Переменные окружения
Создайте файл .env в корне проекта:

env
EXCHANGE_API_KEY=your_api_key_here
API ключ можно получить на exchangeratesapi.io

## Новые форматы данных

Проект теперь поддерживает чтение финансовых транзакций из **CSV** и **Excel (XLSX)** файлов.

### Функции

| Функция | Формат | Возвращает |
|---------|--------|------------|
| `read_csv_transactions(file_path)` | CSV | `List[Dict[str, Any]]` |
| `read_excel_transactions(file_path)` | Excel (XLSX) | `List[Dict[str, Any]]` |

### Пример использования

```python
from src.file_reader import read_csv_transactions, read_excel_transactions

# Чтение CSV
transactions_csv = read_csv_transactions("data/transactions.csv")

# Чтение Excel
transactions_excel = read_excel_transactions("data/transactions_excel.xlsx")

print(f"CSV: {len(transactions_csv)} транзакций")
print(f"Excel: {len(transactions_excel)} транзакций")
```
## Интерактивный режим работы

Запустите `main.py` для работы с программой через консоль:
- Выбор источника данных (JSON, CSV, XLSX)
- Фильтрация по статусу (EXECUTED, CANCELED, PENDING)
- Сортировка по дате
- Фильтрация по рублёвым транзакциям
- Поиск по слову в описании с использованием регулярных выражений

### Пример работы

```
poetry run python main.py
Поиск транзакций
Функция search_transactions(transactions, search_string) — ищет транзакции, содержащие заданную строку в описании (регистронезависимо, с поддержкой re).

python
from src.search_utils import search_transactions

result = search_transactions(transactions, "Перевод")
Подсчёт категорий
Функция count_operations_by_category(transactions, categories) — подсчитывает количество операций в каждой категории с использованием Counter.

python
from src.processing import count_operations_by_category

categories = ['Перевод', 'Вклад', 'Покупка']
result = count_operations_by_category(transactions, categories)
text

```
## Курсовая работа — анализ банковских транзакций

### Веб-страницы

#### Главная (`main_page`)

Возвращает JSON с данными для главной страницы:
- Приветствие в зависимости от времени суток
- Информация по каждой карте (последние 4 цифры, сумма расходов, кешбэк)
- Топ-5 транзакций по сумме
- Курсы валют из `user_settings.json`
- Цены акций из `user_settings.json`

#### События (`events_page`)

Анализ расходов и доходов за выбранный период (месяц, неделя, год, всё время).  
Возвращает JSON с:
- Общей суммой расходов и доходов
- Топ-7 категориями расходов (остальные в «Остальное»)
- Отдельными категориями «Переводы» и «Наличные»
- Курсами валют и ценами акций

### Сервисы

#### Поиск транзакций (`search_transactions`, `main_search`)

Поиск по описанию или категории (регистронезависимый).  
Пример: `main_search("перевод")` вернёт все транзакции с этим словом.

#### Поиск по телефонным номерам (`search_phone_numbers`, `main_phone_search`)

Находит транзакции, содержащие номера телефонов в описании.  
Поддерживаются форматы: `+7 921 11-22-33`, `89000000000`, `+7 (900) 000-00-00` и др.

#### Топ-3 категории кешбэка (`top_cashback_categories`)

Анализирует, какие категории принесли наибольший кешбэк за период.

### Отчёты

#### Траты по категории (`spending_by_category`)

Возвращает траты по заданной категории за последние 3 месяца от указанной даты.  
Результат сохраняется в JSON-файл (через декоратор `@report_decorator`).


---
## Лицензия

MIT
