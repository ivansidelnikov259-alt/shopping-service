"""
Сервис учета покупок и формирования списка покупок
Начальная версия - Практическая работа №1
"""

import datetime
import sys

# Простые типы данных
APP_VERSION = "0.1.0"
APP_NAME = "Shopping Service"


def print_header():
    """Выводит заголовок приложения"""
    print("=" * 50)
    print(f"{APP_NAME} v{APP_VERSION}")
    print("Сервис учета покупок и формирования списка покупок")
    print("=" * 50)


def get_user_choice():
    """Получает выбор пользователя из меню"""
    print("\nГлавное меню:")
    print("1. Добавить покупку")
    print("2. Показать все покупки")
    print("3. Показать итоги по категориям")
    print("4. Создать список покупок")
    print("5. Выход")
    
    choice = input("\nВыберите действие (1-5): ")
    return choice


def add_purchase(purchases):
    """Добавляет новую покупку"""
    print("\n--- Добавление новой покупки ---")
    
    # Ввод названия товара
    product_name = input("Введите название товара: ").strip()
    if not product_name:
        print("Ошибка: название товара не может быть пустым")
        return
    
    # Ввод цены с преобразованием типов
    price_input = input("Введите цену (руб): ").strip()
    try:
        price = float(price_input)
        if price <= 0:
            print("Ошибка: цена должна быть больше нуля")
            return
    except ValueError:
        print("Ошибка: введите корректное число")
        return
    
    # Ввод категории
    category = input("Введите категорию товара: ").strip()
    if not category:
        print("Ошибка: категория не может быть пустой")
        return
    
    # Ввод магазина
    store = input("Введите название магазина: ").strip()
    if not store:
        store = "Не указан"
    
    # Ввод даты покупки
    date_input = input("Введите дату покупки (ДД.ММ.ГГГГ, нажмите Enter для сегодняшней даты): ").strip()
    
    if date_input:
        try:
            # Преобразование строки в дату
            day, month, year = date_input.split('.')
            purchase_date = datetime.date(int(year), int(month), int(day))
        except (ValueError, TypeError):
            print("Ошибка: неверный формат даты. Используйте ДД.ММ.ГГГГ")
            return
    else:
        purchase_date = datetime.date.today()
    
    # Создание словаря с данными покупки
    purchase = {
        "product": product_name,
        "price": price,
        "category": category,
        "store": store,
        "date": purchase_date,
        "id": len(purchases) + 1
    }
    
    purchases.append(purchase)
    print(f"\n✅ Покупка '{product_name}' успешно добавлена!")


def show_all_purchases(purchases):
    """Показывает все покупки"""
    print("\n--- Все покупки ---")
    
    if not purchases:
        print("Список покупок пуст")
        return
    
    total_sum = 0
    for purchase in purchases:
        print(f"\nПокупка #{purchase['id']}:")
        print(f"  Товар: {purchase['product']}")
        print(f"  Цена: {purchase['price']:.2f} руб.")
        print(f"  Категория: {purchase['category']}")
        print(f"  Магазин: {purchase['store']}")
        print(f"  Дата: {purchase['date'].strftime('%d.%m.%Y')}")
        total_sum += purchase['price']
    
    print(f"\nВсего покупок: {len(purchases)}")
    print(f"Общая сумма: {total_sum:.2f} руб.")


def show_categories_summary(purchases):
    """Показывает итоги по категориям"""
    print("\n--- Итоги по категориям ---")
    
    if not purchases:
        print("Нет данных для анализа")
        return
    
    # Простой подсчет по категориям (без использования сложных структур)
    categories = []
    sums = []
    
    for purchase in purchases:
        category = purchase['category']
        price = purchase['price']
        
        # Проверяем, есть ли уже такая категория
        found = False
        for i in range(len(categories)):
            if categories[i] == category:
                sums[i] += price
                found = True
                break
        
        if not found:
            categories.append(category)
            sums.append(price)
    
    print("\nИтоги по категориям:")
    for i in range(len(categories)):
        print(f"  {categories[i]}: {sums[i]:.2f} руб.")


def create_shopping_list():
    """Создает список покупок"""
    print("\n--- Создание списка покупок ---")
    
    list_name = input("Введите название списка: ").strip()
    if not list_name:
        print("Ошибка: название списка не может быть пустым")
        return
    
    print(f"\nСписок '{list_name}' создан!")
    print("Теперь добавляйте товары в список (введите 'stop' для завершения):")
    
    items = []
    item_number = 1
    
    while True:
        item = input(f"Товар {item_number}: ").strip()
        
        if item.lower() == 'stop' or item.lower() == 'стоп':
            break
        
        if item:
            items.append(item)
            item_number += 1
    
    if items:
        print(f"\nСписок '{list_name}':")
        for i, item in enumerate(items, 1):
            print(f"  {i}. {item}")
        print(f"Всего товаров: {len(items)}")
    else:
        print(f"\nСписок '{list_name}' пуст")


def main():
    """Главная функция приложения"""
    
    # Список для хранения покупок (простая структура)
    purchases = []
    
    # Вывод информации о системе
    print_header()
    
    # Проверка версии Python (ветвление)
    python_version = sys.version_info
    
    if python_version.major >= 3 and python_version.minor >= 7:
        print(f"Python {python_version.major}.{python_version.minor}.{python_version.micro}")
        print("✅ Система готова к работе")
    else:
        print("❌ Требуется Python 3.7 или выше")
        return
    
    # Основной цикл программы
    while True:
        choice = get_user_choice()
        
        # Ветвление для обработки выбора пользователя
        if choice == "1":
            add_purchase(purchases)
        elif choice == "2":
            show_all_purchases(purchases)
        elif choice == "3":
            show_categories_summary(purchases)
        elif choice == "4":
            create_shopping_list()
        elif choice == "5":
            print("\nДо свидания! Спасибо за использование сервиса.")
            break
        else:
            print("\n❌ Неверный выбор. Пожалуйста, выберите действие от 1 до 5")


# Точка входа в программу
if __name__ == "__main__":
    main()