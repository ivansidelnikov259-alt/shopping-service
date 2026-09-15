"""
Тесты модуля storage.
"""

import storage
from models import Category, Purchase, ShoppingList, Store


def test_save_and_load_purchases(tmp_path, monkeypatch):
    """Проверяет сохранение и загрузку покупок."""
    monkeypatch.setattr(storage, "DATA_DIR", tmp_path)

    product = Category(category_id=1, name="Продукты")
    store = Store(store_id=1, name="Пятёрочка")

    from datetime import date
    from models import Product

    prod = Product(product_id=1, name="Молоко", price=89.9, category=product)

    purchase = Purchase(
        purchase_id=1,
        product=prod,
        price=89.9,
        category=product,
        store=store,
        purchase_date=date(2026, 9, 15),
    )

    assert storage.save_purchases([purchase]) is True

    loaded = storage.load_purchases()
    assert len(loaded) == 1
    assert loaded[0].product.name == "Молоко"
    assert loaded[0].price == 89.9


def test_save_and_load_shopping_lists(tmp_path, monkeypatch):
    """Проверяет сохранение и загрузку списков покупок."""
    monkeypatch.setattr(storage, "DATA_DIR", tmp_path)

    sl = ShoppingList(list_id=1, name="На выходные")
    assert storage.save_shopping_lists([sl]) is True

    loaded = storage.load_shopping_lists()
    assert len(loaded) == 1
    assert loaded[0].name == "На выходные"


def test_load_empty_file(tmp_path, monkeypatch):
    """Проверяет, что при отсутствии файла возвращается пустой список."""
    monkeypatch.setattr(storage, "DATA_DIR", tmp_path)
    assert storage.load_purchases() == []
    assert storage.load_shopping_lists() == []


def test_save_and_load_categories(tmp_path, monkeypatch):
    """Проверяет сохранение и загрузку категорий."""
    monkeypatch.setattr(storage, "DATA_DIR", tmp_path)
    cats = [Category(category_id=1, name="Продукты")]
    assert storage.save_categories(cats) is True

    loaded = storage.load_categories()
    assert len(loaded) == 1
    assert loaded[0].name == "Продукты"


def test_save_and_load_stores(tmp_path, monkeypatch):
    """Проверяет сохранение и загрузку магазинов."""
    monkeypatch.setattr(storage, "DATA_DIR", tmp_path)
    stores = [Store(store_id=1, name="Пятёрочка", address="ул. Ленина, 1")]
    assert storage.save_stores(stores) is True

    loaded = storage.load_stores()
    assert len(loaded) == 1
    assert loaded[0].name == "Пятёрочка"
    assert loaded[0].address == "ул. Ленина, 1"
