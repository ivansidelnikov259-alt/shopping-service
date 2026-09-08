"""
Сервис учета покупок и формирования списка покупок.
Практическая работа №2: коллекции, функции, циклы, файлы.
"""

from datetime import datetime
from typing import List, Dict

from storage import load_data, save_data
from utils import input_float, input_non_empty, input_date, input_int

APP_VERSION = "0.2.0"
APP_NAME = "Shopping Service"

PURCHASES_FILE = "purchases.json"
SHOPPING_LISTS_FILE = "shopping_lists.json"


def print_header() -> None:
    """Выводит заголовок приложения."""
    print("=" * 50)
    print(f"{APP_NAME} v{APP_VERSION}")
    print("Сервис учета покупок и формирования списка покупок")
    print("=" * 50)


def print_menu() -> None:
    """Выводит главное меню."""
    print("\nГлавное меню:")
    print("1. Добавить покупку")
    print("2. Показать все покупки")
    print("3. Показать итоги по категориям")
    print("4. Найти покупки по названию")
    print("5. Создать список покупок")
    print("6. Показать списки покупок")
    print("7. Удалить покупку")
    print("8. Выход")


def get_user_choice() -> str:
    """
    Получает выбор пользователя из меню.

    Returns:
        Строку с выбором пользователя.
    """
    print_menu()
    choice = input("\nВыберите действие (1-8): ").strip()
    return choice


def add_purchase(purchases: List[dict]) -> None:
    """
    Добавляет новую покупку.

    Args:
        purchases: Список покупок.
    """
    print("\n--- Добавление новой покупки ---")

    product_name = input_non_empty("Введите название товара: ")
    price = input_float("Введите цену (руб): ")
    category = input_non_empty("Введите категорию товара: ")
    store = input("Введите название магазина (Enter - не указан): ").strip()
    if not store:
        store = "Не указан"

    purchase_date = input_date("Введите дату покупки (ДД.ММ.ГГГГ, Enter - сегодня): ")

    purchase = {
        "id": get_next_id(purchases),
        "product": product_name,
        "price": price,
        "category": category,
        "store": store,
        "date": purchase_date.isoformat(),
        "created_at": datetime.now().isoformat()
    }

    purchases.append(purchase)

    if save_data(PURCHASES_FILE, purchases):
        print(f"\n✅ Покупка '{product_name}' успешно добавлена!")
    else:
        print("\n❌ Ошибка при сохранении покупки")


def get_next_id(items: List[dict]) -> int:
    """
    Возвращает следующий свободный ID.

    Args:
        items: Список элементов.

    Returns:
        Следующий ID.
    """
    if not items:
        return 1

    max_id = max(item.get("id", 0) for item in items)
    return max_id + 1


def show_all_purchases(purchases: List[dict]) -> None:
    """
    Показывает все покупки.

    Args:
        purchases: Список покупок.
    """
    print("\n--- Все покупки ---")

    if not purchases:
        print("Список покупок пуст")
        return

    total_sum = 0.0

    print(f"\n{'ID':<5} {'Товар':<20} {'Цена':<10} {'Категория':<15} {'Магазин':<15} {'Дата':<12}")
    print("-" * 77)

    for purchase in purchases:
        print(f"{purchase['id']:<5} {purchase['product']:<20} {purchase['price']:<10.2f} "
              f"{purchase['category']:<15} {purchase['store']:<15} {purchase['date']:<12}")
        total_sum += purchase["price"]

    print("-" * 77)
    print(f"Всего покупок: {len(purchases)}")
    print(f"Общая сумма: {total_sum:.2f} руб.")


def show_categories_summary(purchases: List[dict]) -> None:
    """
    Показывает итоги по категориям.

    Args:
        purchases: Список покупок.
    """
    print("\n--- Итоги по категориям ---")

    if not purchases:
        print("Нет данных для анализа")
        return

    categories: Dict[str, float] = {}

    for purchase in purchases:
        category = purchase["category"]
        price = purchase["price"]

        if category in categories:
            categories[category] += price
        else:
            categories[category] = price

    print(f"\n{'Категория':<20} {'Сумма':<15} {'Кол-во':<10}")
    print("-" * 45)

    for category, total in sorted(categories.items(), key=lambda x: x[1], reverse=True):
        count = sum(1 for p in purchases if p["category"] == category)
        print(f"{category:<20} {total:<15.2f} {count:<10}")

    print("-" * 45)
    print(f"Всего категорий: {len(categories)}")


def find_purchases(purchases: List[dict]) -> None:
    """
    Ищет покупки по названию товара.

    Args:
        purchases: Список покупок.
    """
    print("\n--- Поиск покупок ---")

    query = input("Введите название товара для поиска: ").strip().lower()

    if not query:
        print("Ошибка: введите название для поиска")
        return

    found = [p for p in purchases if query in p["product"].lower()]

    if not found:
        print(f"Покупки с названием '{query}' не найдены")
        return

    print(f"\nНайдено покупок: {len(found)}")
    for purchase in found:
        print(f"  #{purchase['id']}: {purchase['product']} - {purchase['price']:.2f} руб. "
              f"({purchase['category']}, {purchase['date']})")


def create_shopping_list(shopping_lists: List[dict]) -> None:
    """
    Создает новый список покупок.

    Args:
        shopping_lists: Список списков покупок.
    """
    print("\n--- Создание списка покупок ---")

    list_name = input_non_empty("Введите название списка: ")

    print(f"\nСписок '{list_name}' создан!")
    print("Добавляйте товары (введите 'stop' для завершения):")

    items: List[str] = []
    item_number = 1

    while True:
        item = input(f"Товар {item_number}: ").strip()

        if item.lower() in ("stop", "стоп"):
            break

        if item:
            items.append(item)
            item_number += 1

    new_list = {
        "id": get_next_id(shopping_lists),
        "name": list_name,
        "items": items,
        "created_at": datetime.now().isoformat()
    }

    shopping_lists.append(new_list)

    if save_data(SHOPPING_LISTS_FILE, shopping_lists):
        print(f"\n✅ Список '{list_name}' сохранен!")
        if items:
            print(f"Товаров в списке: {len(items)}")
    else:
        print("\n❌ Ошибка при сохранении списка")


def show_shopping_lists(shopping_lists: List[dict]) -> None:
    """
    Показывает все списки покупок.

    Args:
        shopping_lists: Список списков покупок.
    """
    print("\n--- Списки покупок ---")

    if not shopping_lists:
        print("Списки покупок отсутствуют")
        return

    for shopping_list in shopping_lists:
        print(f"\nСписок #{shopping_list['id']}: {shopping_list['name']}")
        print(f"Создан: {shopping_list['created_at'][:10]}")

        if shopping_list["items"]:
            print("Товары:")
            for i, item in enumerate(shopping_list["items"], 1):
                print(f"  {i}. {item}")
            print(f"Всего товаров: {len(shopping_list['items'])}")
        else:
            print("Список пуст")


def delete_purchase(purchases: List[dict]) -> None:
    """
    Удаляет покупку по ID.

    Args:
        purchases: Список покупок.
    """
    print("\n--- Удаление покупки ---")

    if not purchases:
        print("Список покупок пуст")
        return

    show_all_purchases(purchases)

    purchase_id = input_int("Введите ID покупки для удаления: ")

    for i, purchase in enumerate(purchases):
        if purchase["id"] == purchase_id:
            deleted = purchases.pop(i)
            if save_data(PURCHASES_FILE, purchases):
                print(f"\n✅ Покупка '{deleted['product']}' удалена!")
            else:
                print("\n❌ Ошибка при сохранении изменений")
            return

    print(f"\n❌ Покупка с ID {purchase_id} не найдена")


def main() -> None:
    """Главная функция приложения."""
    print_header()

    # Загрузка данных из файлов
    purchases = load_data(PURCHASES_FILE)
    shopping_lists = load_data(SHOPPING_LISTS_FILE)

    print(f"Загружено покупок: {len(purchases)}")
    print(f"Загружено списков: {len(shopping_lists)}")

    while True:
        choice = get_user_choice()

        if choice == "1":
            add_purchase(purchases)
        elif choice == "2":
            show_all_purchases(purchases)
        elif choice == "3":
            show_categories_summary(purchases)
        elif choice == "4":
            find_purchases(purchases)
        elif choice == "5":
            create_shopping_list(shopping_lists)
        elif choice == "6":
            show_shopping_lists(shopping_lists)
        elif choice == "7":
            delete_purchase(purchases)
        elif choice == "8":
            print("\nДо свидания! Спасибо за использование сервиса.")
            break
        else:
            print("\n❌ Неверный выбор. Пожалуйста, выберите действие от 1 до 8")


if __name__ == "__main__":
    main()
