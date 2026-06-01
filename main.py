"""
Главный модуль проекта bank_widget.
"""

from src.file_reader import read_csv_transactions, read_excel_transactions
from src.processing import filter_by_state, sort_by_date
from src.search_utils import search_transactions
from src.utils import load_transactions


def get_valid_status() -> str:
    """Запрашивает у пользователя статус операции и возвращает его."""
    valid_statuses = ['EXECUTED', 'CANCELED', 'PENDING']

    while True:
        print("\nВведите статус, по которому необходимо выполнить фильтрацию.")
        print("Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING")
        status = input().strip().upper()

        if status in valid_statuses:
            print(f"Операции отфильтрованы по статусу \"{status}\"")
            return status
        else:
            print(f"Статус операции \"{status}\" недоступен.")


def get_bool_input(prompt: str) -> bool:
    """Запрашивает у пользователя ответ Да/Нет и возвращает bool."""
    while True:
        answer = input(f"{prompt} Да/Нет\n").strip().lower()
        if answer in ['да', 'yes', 'y', 'д']:
            return True
        elif answer in ['нет', 'no', 'n']:
            return False
        else:
            print("Пожалуйста, ответьте 'Да' или 'Нет'")


def get_sort_order() -> str:
    """Запрашивает направление сортировки."""
    while True:
        print("Отсортировать по возрастанию или по убыванию?")
        order = input().strip().lower()
        if order in ['по возрастанию', 'возрастанию', 'asc', 'ascending']:
            return 'asc'
        elif order in ['по убыванию', 'убыванию', 'desc', 'descending']:
            return 'desc'
        else:
            print("Пожалуйста, введите 'по возрастанию' или 'по убыванию'")


def format_transaction(transaction: dict) -> str:
    """Форматирует одну транзакцию для вывода в консоль."""
    date = transaction.get('date', '')[:10].replace('-', '.')
    description = transaction.get('description', '')
    amount = transaction.get('amount', 0)
    currency = transaction.get('currency', {}).get('code', 'RUB')

    return f"{date} {description}\nСумма: {amount} {currency}."


def main():
    """Основная функция программы."""
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    choice = input().strip()

    transactions = []
    if choice == '1':
        print("Для обработки выбран JSON-файл.")
        transactions = load_transactions('data/operations.json')
    elif choice == '2':
        print("Для обработки выбран CSV-файл.")
        transactions = read_csv_transactions('data/transactions.csv')
    elif choice == '3':
        print("Для обработки выбран XLSX-файл.")
        transactions = read_excel_transactions('data/transactions_excel.xlsx')
    else:
        print("Неверный выбор. Завершение программы.")
        return

    if not transactions:
        print("Не удалось загрузить транзакции. Проверьте наличие файлов.")
        return

    # Фильтрация по статусу
    status = get_valid_status()
    filtered = filter_by_state(transactions, status)

    if not filtered:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
        return

    # Сортировка по дате
    if get_bool_input("Отсортировать операции по дате?"):
        order = get_sort_order()
        filtered = sort_by_date(filtered, descending=(order == 'desc'))

    # Фильтрация по рублям
    if get_bool_input("Выводить только рублевые транзакции?"):
        filtered = [t for t in filtered if t.get('currency', {}).get('code') == 'RUB']

    # Поиск по слову в описании
    if get_bool_input("Отфильтровать список транзакций по определенному слову в описании?"):
        search_word = input("Введите слово для поиска:\n").strip()
        filtered = search_transactions(filtered, search_word)

    if not filtered:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
        return

    print("\nРаспечатываю итоговый список транзакций...")
    print(f"Всего банковских операций в выборке: {len(filtered)}")
    print()

    for transaction in filtered:
        print(format_transaction(transaction))
        print()


if __name__ == "__main__":
    main()
