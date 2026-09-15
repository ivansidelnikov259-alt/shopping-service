"""
Тесты моделей предметной области.
"""

from datetime import date

from models import Category, Product, Store, User
from models.category import add_category, find_category_by_name
from models.purchase import (
    add_purchase,
    delete_purchase,
    find_purchases_by_name,
    get_categories_summary,
    get_total_sum,
)
from models.shopping_list import add_shopping_list, delete_shopping_list
from models.store import add_store
from models.product import add_product


def test_category_creation():
    """Проверяет создание категории."""
    cat = Category(category_id=1, name="Продукты")
    assert cat.id == 1
    assert cat.name == "Продукты"
    assert "Продукты" in str(cat)


def test_store_creation():
    """Проверяет создание магазина."""
    store = Store(store_id=1, name="Пятёрочка")
    assert store.id == 1
    assert store.name == "Пятёрочка"
    assert "Пятёрочка" in str(store)


def test_product_creation():
    """Проверяет создание товара."""
    cat = Category(category_id=1, name="Продукты")
    prod = Product(product_id=1, name="Молоко", price=89.9, category=cat)
    assert prod.name == "Молоко"
    assert prod.price == 89.9
    assert prod.category is cat


def test_user_creation():
    """Проверяет создание пользователя."""
    user = User(user_id=1, name="Иван Петров", email="ivan@example.com")
    assert user.name == "Иван Петров"
    assert user.email == "ivan@example.com"


def test_add_category():
    """Проверяет добавление категории в коллекцию."""
    cats = []
    add_category(cats, "Продукты")
    add_category(cats, "Бытовая химия")

    assert len(cats) == 2
    assert find_category_by_name(cats, "Продукты") is not None


def test_add_store():
    """Проверяет добавление магазина."""
    stores = []
    add_store(stores, "Пятёрочка")
    add_store(stores, "Магнит")

    assert len(stores) == 2
    assert stores[0].name == "Пятёрочка"


def test_add_product():
    """Проверяет добавление товара."""
    products = []
    add_product(products, "Молоко", 89.9)
    assert len(products) == 1
    assert products[0].name == "Молоко"


def test_add_purchase():
    """Проверяет добавление покупки."""
    cat = Category(category_id=1, name="Продукты")
    store = Store(store_id=1, name="Пятёрочка")
    prod = Product(product_id=1, name="Молоко", price=89.9, category=cat)

    purchases = []
    purchase = add_purchase(
        purchases=purchases,
        product=prod,
        price=89.9,
        category=cat,
        store=store,
        purchase_date=date(2026, 9, 15),
    )

    assert len(purchases) == 1
    assert purchase.product.name == "Молоко"
    assert purchase.price == 89.9


def test_delete_purchase():
    """Проверяет удаление покупки."""
    cat = Category(category_id=1, name="Продукты")
    store = Store(store_id=1, name="Пятёрочка")
    prod = Product(product_id=1, name="Молоко", price=89.9, category=cat)

    purchases = []
    purchase = add_purchase(
        purchases, prod, 89.9, cat, store, date(2026, 9, 15)
    )

    assert delete_purchase(purchases, purchase.id) is True
    assert len(purchases) == 0


def test_total_sum_and_categories_summary():
    """Проверяет подсчёт суммы и группировку по категориям."""
    cat1 = Category(category_id=1, name="Продукты")
    cat2 = Category(category_id=2, name="Бытовая химия")
    store = Store(store_id=1, name="Пятёрочка")

    prod1 = Product(product_id=1, name="Молоко", price=89.9, category=cat1)
    prod2 = Product(product_id=2, name="Мыло", price=50.0, category=cat2)

    purchases = []
    add_purchase(purchases, prod1, 89.9, cat1, store, date(2026, 9, 15))
    add_purchase(purchases, prod2, 50.0, cat2, store, date(2026, 9, 15))

    assert get_total_sum(purchases) == 139.9

    summary = get_categories_summary(purchases)
    assert summary["Продукты"] == 89.9
    assert summary["Бытовая химия"] == 50.0


def test_find_purchases_by_name():
    """Проверяет поиск покупок по части названия."""
    cat = Category(category_id=1, name="Продукты")
    store = Store(store_id=1, name="Пятёрочка")
    prod = Product(product_id=1, name="Молоко", price=89.9, category=cat)

    purchases = []
    add_purchase(purchases, prod, 89.9, cat, store, date(2026, 9, 15))

    assert len(find_purchases_by_name(purchases, "мол")) == 1
    assert len(find_purchases_by_name(purchases, "хлеб")) == 0


def test_shopping_list():
    """Проверяет создание списка и добавление товаров."""
    sls = []
    sl = add_shopping_list(sls, "На выходные")

    prod1 = Product(product_id=1, name="Сыр", price=320.0)
    prod2 = Product(product_id=2, name="Масло", price=150.0)

    sl.add_item(prod1)
    sl.add_item(prod2)

    assert len(sl.items) == 2
    assert sl.total == 470.0

    assert delete_shopping_list(sls, sl.id) is True
    assert len(sls) == 0
