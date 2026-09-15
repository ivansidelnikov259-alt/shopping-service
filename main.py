"""
Сервис учёта покупок и формирования списка покупок.

Практическая работа №3: объектно-ориентированное программирование.
Точка входа и пользовательский интерфейс.
"""

from typing import List

from models import Category, Product, Purchase, ShoppingList, Store
from models.category import get_or_create_category, show_categories
from models.product import show_products
from models.purchase import (
    add_purchase,
    delete_purchase,
    find_purchases_by_name,
    get_categories_summary,
    get_total_sum,
    show_purchases,
)
from models.shopping_list import (
    add_shopping_list,
    delete_shopping_list,
    show_shopping_lists,
)
from models.store import get_or_create_store, show_stores
from storage import (
    load_categories,
    load_purchases,
    load_shopping_lists,
    load_stores,
    save_categories,
    save_purchases,
    save_shopping_lists,
    save_stores,
)
from utils import input_date, input_float, input_int, input_non_empty

APP_VERSION = "0.3.0"
APP_NAME = "Shopping Service"


def print_header() -> None:
    """Выводит заголовок приложения."""
    print("=" * 60)
    print(f"{APP_NAME} v{APP_VERSION}")
    print("Сервис учёта покупок и формирования списка покупок")
    print("=" * 60)


def print_menu() -> None:
    """Выводит главное меню."""
    print("\nГлавное меню:")
    print("1.  Добавить покупку")
    print("2.  Показать все покупки")
    print("3.  Показать итоги по категориям")
    print("4.  Найти покупки по названию")
    print("5.  Удалить покупку")
    print("6.  Создать список покупок")
    print("7.  Показать списки покупок")
    print("8.  Удалить список покупок")
    print("9.  Показать все категории")
    print("10. Показать все магазины")
    print("11. Показать все товары")
    print("12. Выход")


def get_user_choice() -> str:
    """Получает выбор пользователя из меню."""
    print_menu()
    return input("\nВыберите действие (1-12): ").strip()


# ---------- Пользовательские сценарии ----------


def create_purchase(
    purchases: List[Purchase],
    categories: List[Category],
    stores: List[Store],
) -> None:
    """
    Сценарий создания новой покупки.

    Args:
        purchases: Коллекция покупок.
        categories: Коллекция категорий.
        stores: Коллекция магазинов.
    """
    print("\n--- Добавление новой покупки ---")

    product_name = input_non_empty("Введите название товара: ")
    price = input_float("Введите цену (руб): ")

    category_name = input_non_empty("Введите категорию товара: ")
    category = get_or_create_category(categories, category_name)

    store_name = input("Введите название магазина (Enter — не указан): ").strip()
    if not store_name:
        store_name = "Не указан"
    store = get_or_create_store(stores, store_name)

    purchase_date = input_date(
        "Введите дату покупки (ДД.ММ.ГГГГ, Enter — сегодня): "
    )

    product = Product(
        product_id=0,
        name=product_name,
        price=price,
        category=category,
    )

    purchase = add_purchase(
        purchases=purchases,
        product=product,
        price=price,
        category=category,
        store=store,
        purchase_date=purchase_date,
    )

    save_purchases(purchases)
    save_categories(categories)
    save_stores(stores)

    print(f"\n✅ Покупка создана: {purchase}")


def search_purchases(purchases: List[Purchase]) -> None:
    """Сценарий поиска покупок по названию."""
    print("\n--- Поиск покупок ---")
    query = input("Введите часть названия товара: ").strip()

    if not query:
        print("Ошибка: пустой запрос")
        return

    found = find_purchases_by_name(purchases, query)
    if not found:
        print(f"Покупки по запросу '{query}' не найдены")
        return

    print(f"\nНайдено покупок: {len(found)}")
    for purchase in found:
        print(f"  {purchase}")


def remove_purchase(purchases: List[Purchase]) -> None:
    """Сценарий удаления покупки."""
    print("\n--- Удаление покупки ---")
    if not purchases:
        print("Покупки отсутствуют")
        return

    show_purchases(purchases)
    purchase_id = input_int("Введите ID покупки для удаления: ")

    if delete_purchase(purchases, purchase_id):
        save_purchases(purchases)
        print(f"\n✅ Покупка #{purchase_id} удалена")
    else:
        print(f"\n❌ Покупка #{purchase_id} не найдена")


def create_list(shopping_lists: List[ShoppingList]) -> None:
    """Сценарий создания списка покупок."""
    print("\n--- Создание списка покупок ---")
    list_name = input_non_empty("Введите название списка: ")

    shopping_list = add_shopping_list(shopping_lists, list_name)

    print(f"\nСписок '{list_name}' создан!")
    print("Добавляйте товары (введите 'stop' для завершения):")

    counter = 1
    while True:
        item_name = input(f"Товар {counter}: ").strip()
        if item_name.lower() in ("stop", "стоп"):
            break
        if not item_name:
            continue
        price_input = input(f"  Цена товара '{item_name}': ").strip()
        try:
            price = float(price_input)
        except ValueError:
            print("  Ошибка: цена должна быть числом, товар не добавлен")
            continue

        product = Product(
            product_id=counter,
            name=item_name,
            price=price,
        )
        shopping_list.add_item(product)
        counter += 1

    save_shopping_lists(shopping_lists)
    print(f"\n✅ Список сохранён: {shopping_list}")
    if shopping_list.items:
        print(f"   Итого: {shopping_list.get_total():.2f} руб.")


def remove_list(shopping_lists: List[ShoppingList]) -> None:
    """Сценарий удаления списка покупок."""
    print("\n--- Удаление списка покупок ---")
    if not shopping_lists:
        print("Списки отсутствуют")
        return

    show_shopping_lists(shopping_lists)
    list_id = input_int("Введите ID списка для удаления: ")

    if delete_shopping_list(shopping_lists, list_id):
        save_shopping_lists(shopping_lists)
        print(f"\n✅ Список #{list_id} удалён")
    else:
        print(f"\n❌ Список #{list_id} не найден")


def print_categories_summary(purchases: List[Purchase]) -> None:
    """Выводит итоги по категориям."""
    print("\n--- Итоги по категориям ---")
    if not purchases:
        print("Покупки отсутствуют")
        return

    summary = get_categories_summary(purchases)
    print(f"\n{'Категория':<25} {'Сумма':>15}")
    print("-" * 42)
    for name, total in sorted(summary.items(), key=lambda x: x[1], reverse=True):
        print(f"{name:<25} {total:>15.2f}")
    print("-" * 42)
    print(f"Всего покупок: {len(purchases)}")
    print(f"Общая сумма: {get_total_sum(purchases):.2f} руб.")


# ---------- Главная функция ----------


def main() -> None:
    """Главная функция приложения."""
    print_header()

    # Загрузка данных из файлов в виде объектов
    categories = load_categories()
    stores = load_stores()
    purchases = load_purchases()
    shopping_lists = load_shopping_lists()

    print(f"Загружено покупок: {len(purchases)}")
    print(f"Загружено списков: {len(shopping_lists)}")
    print(f"Загружено категорий: {len(categories)}")
    print(f"Загружено магазинов: {len(stores)}")

    while True:
        choice = get_user_choice()

        if choice == "1":
            create_purchase(purchases, categories, stores)
        elif choice == "2":
            show_purchases(purchases)
        elif choice == "3":
            print_categories_summary(purchases)
        elif choice == "4":
            search_purchases(purchases)
        elif choice == "5":
            remove_purchase(purchases)
        elif choice == "6":
            create_list(shopping_lists)
        elif choice == "7":
            show_shopping_lists(shopping_lists)
        elif choice == "8":
            remove_list(shopping_lists)
        elif choice == "9":
            show_categories(categories)
        elif choice == "10":
            show_stores(stores)
        elif choice == "11":
            all_products = [p.product for p in purchases]
            show_products(all_products)
        elif choice == "12":
            save_purchases(purchases)
            save_shopping_lists(shopping_lists)
            save_categories(categories)
            save_stores(stores)
            print("\nДо свидания! Спасибо за использование сервиса.")
            break
        else:
            print("\n❌ Неверный выбор. Введите число от 1 до 12")


if __name__ == "__main__":
    main()
