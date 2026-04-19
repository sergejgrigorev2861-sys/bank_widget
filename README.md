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

## Лицензия

MIT