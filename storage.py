"""
Модуль для работы с файловым хранилищем данных.

Выполняет преобразование:
- JSON → объекты Python
- объекты Python → JSON
"""

import json
from pathlib import Path
from typing import List

from models import Category, Product, Purchase, ShoppingList, Store, User

# Путь к папке с данными
DATA_DIR = Path("data")


def ensure_data_dir() -> None:
    """Создает папку для данных, если она не существует."""
    DATA_DIR.mkdir(exist_ok=True)


# ---------- Универсальные функции JSON ----------


def load_raw_data(filename: str) -> List[dict]:
    """
    Загружает «сырые» данные из JSON файла.

    Args:
        filename: Имя файла.

    Returns:
        Список словарей с данными.
    """
    filepath = DATA_DIR / filename

    if not filepath.exists():
        return []

    try:
        with open(filepath, "r", encoding="utf-8") as file:
            data = json.load(file)
            if isinstance(data, list):
                return data
            return []
    except (json.JSONDecodeError, OSError):
        return []


def save_raw_data(filename: str, data: List[dict]) -> bool:
    """
    Сохраняет «сырые» данные в JSON файл.

    Args:
        filename: Имя файла.
        data: Список словарей.

    Returns:
        True, если сохранение успешно.
    """
    ensure_data_dir()
    filepath = DATA_DIR / filename

    try:
        with open(filepath, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2, default=str)
        return True
    except OSError:
        return False


# ---------- Покупки ----------


def load_purchases(filename: str = "purchases.json") -> List[Purchase]:
    """
    Загружает покупки из JSON и преобразует их в объекты Purchase.

    Args:
        filename: Имя файла.

    Returns:
        Список объектов Purchase.
    """
    raw = load_raw_data(filename)
    return [Purchase.from_data(item) for item in raw]


def save_purchases(
    purchases: List[Purchase],
    filename: str = "purchases.json",
) -> bool:
    """
    Сохраняет объекты Purchase в JSON.

    Args:
        purchases: Список объектов Purchase.
        filename: Имя файла.

    Returns:
        True, если сохранение успешно.
    """
    data = [purchase.to_dict() for purchase in purchases]
    return save_raw_data(filename, data)


# ---------- Списки покупок ----------


def load_shopping_lists(
    filename: str = "shopping_lists.json",
) -> List[ShoppingList]:
    """Загружает списки покупок из JSON в объекты ShoppingList."""
    raw = load_raw_data(filename)
    return [ShoppingList.from_data(item) for item in raw]


def save_shopping_lists(
    shopping_lists: List[ShoppingList],
    filename: str = "shopping_lists.json",
) -> bool:
    """Сохраняет объекты ShoppingList в JSON."""
    data = [sl.to_dict() for sl in shopping_lists]
    return save_raw_data(filename, data)


# ---------- Категории ----------


def load_categories(filename: str = "categories.json") -> List[Category]:
    """Загружает категории из JSON в объекты Category."""
    raw = load_raw_data(filename)
    return [Category.from_data(item) for item in raw]


def save_categories(
    categories: List[Category],
    filename: str = "categories.json",
) -> bool:
    """Сохраняет объекты Category в JSON."""
    data = [cat.to_dict() for cat in categories]
    return save_raw_data(filename, data)


# ---------- Магазины ----------


def load_stores(filename: str = "stores.json") -> List[Store]:
    """Загружает магазины из JSON в объекты Store."""
    raw = load_raw_data(filename)
    return [Store.from_data(item) for item in raw]


def save_stores(
    stores: List[Store],
    filename: str = "stores.json",
) -> bool:
    """Сохраняет объекты Store в JSON."""
    data = [store.to_dict() for store in stores]
    return save_raw_data(filename, data)


# ---------- Товары ----------


def load_products(
    filename: str = "products.json",
    categories: List[Category] | None = None,
) -> List[Product]:
    """Загружает товары из JSON в объекты Product."""
    raw = load_raw_data(filename)
    cats = categories if categories is not None else []
    return [Product.from_data(item, cats) for item in raw]


def save_products(
    products: List[Product],
    filename: str = "products.json",
) -> bool:
    """Сохраняет объекты Product в JSON."""
    data = [product.to_dict() for product in products]
    return save_raw_data(filename, data)


# ---------- Пользователи ----------


def load_users(filename: str = "users.json") -> List[User]:
    """Загружает пользователей из JSON в объекты User."""
    raw = load_raw_data(filename)
    return [User.from_data(item) for item in raw]


def save_users(
    users: List[User],
    filename: str = "users.json",
) -> bool:
    """Сохраняет объекты User в JSON."""
    data = [user.to_dict() for user in users]
    return save_raw_data(filename, data)
