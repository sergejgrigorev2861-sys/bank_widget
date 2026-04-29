# Bank Widget

Виджет для обработки банковских операций клиента.

## Цель проекта

Обеспечить удобную обработку данных о банковских операциях.

## Установка

```bash
git clone git@github.com:sergejgrigorev2861-sys/bank_widget.git
cd bank_widget
```

## Использование

```python
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

```python
from src.generators import filter_by_currency

usd_transactions = filter_by_currency(transactions, "USD")
first_usd = next(usd_transactions)
```

#### `transaction_descriptions(transactions)`
Генератор, возвращающий описания транзакций по очереди.

```python
from src.generators import transaction_descriptions

descriptions = transaction_descriptions(transactions)
for desc in descriptions:
    print(desc)
```

#### `card_number_generator(start, stop)`
Генератор номеров банковских карт в заданном диапазоне.

```python
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

```bash
pytest tests/
```

## Для проверки покрытия

```bash
pytest --cov=src --cov-report=html tests/
```

### Результаты тестирования

- Всего тестов: 19
- Покрытие кода: 100%

## Лицензия

MIT