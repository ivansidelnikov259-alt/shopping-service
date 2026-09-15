"""
Модуль сущности «Товар».

Наследуется от BaseEntity.
"""

from typing import List, Optional

from .base import BaseEntity
from .category import Category


class Product(BaseEntity):
    """
    Товар.

    Дополнительные атрибуты:
        _price: цена.
        _category: объект Category.
    """

    def __init__(
        self,
        product_id: int,
        name: str,
        price: float,
        category: Optional[Category] = None,
    ) -> None:
        """Создать объект товара."""
        super().__init__(entity_id=product_id, name=name)
        self._price = price
        self._category = category

    @property
    def price(self) -> float:
        """Цена товара."""
        return self._price

    @price.setter
    def price(self, value: float) -> None:
        """Установить цену."""
        if value < 0:
            raise ValueError("Цена не может быть отрицательной")
        self._price = value

    @property
    def category(self) -> Optional[Category]:
        """Категория товара."""
        return self._category

    @category.setter
    def category(self, value: Optional[Category]) -> None:
        """Установить категорию."""
        self._category = value

    def __str__(self) -> str:
        """Строковое представление товара."""
        cat_name = self._category.name if self._category else "без категории"
        return f"Товар #{self.id}: {self.name} — {self.price:.2f} руб. ({cat_name})"

    def to_dict(self) -> dict:
        """Преобразовать в словарь."""
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "category_id": self.category.id if self.category else None,
        }

    @classmethod
    def from_data(
        cls, data: dict, categories: List[Category]
    ) -> "Product":
        """Создать объект из словаря."""
        category = None
        cat_id = data.get("category_id")
        if cat_id is not None:
            for cat in categories:
                if cat.id == cat_id:
                    category = cat
                    break
        return cls(
            product_id=data["id"],
            name=data["name"],
            price=data["price"],
            category=category,
        )

    def is_expensive(self, threshold: float = 1000.0) -> bool:
        """Проверить, дороже ли товар порога."""
        return self._price > threshold

    @staticmethod
    def validate_price(price: float) -> bool:
        """Проверить корректность цены."""
        return price >= 0


def get_next_id(products: List[Product]) -> int:
    """Получить следующий свободный ID."""
    if not products:
        return 1
    return max(prod.id for prod in products) + 1


def add_product(
    products: List[Product],
    name: str,
    price: float,
    category: Optional[Category] = None,
) -> Product:
    """Создать новый товар."""
    if not Product.validate_price(price):
        raise ValueError("Некорректная цена")
    new_id = get_next_id(products)
    product = Product(
        product_id=new_id, name=name, price=price, category=category
    )
    products.append(product)
    return product


def find_product_by_id(
    products: List[Product], product_id: int
) -> Optional[Product]:
    """Найти товар по ID."""
    for product in products:
        if product.id == product_id:
            return product
    return None


def find_product_by_name(
    products: List[Product], name: str
) -> Optional[Product]:
    """Найти товар по названию."""
    name_lower = name.lower()
    for product in products:
        if product.name.lower() == name_lower:
            return product
    return None


def filter_products_by_category(
    products: List[Product], category: Category
) -> List[Product]:
    """Отобрать товары по категории."""
    return [prod for prod in products if prod.category is category]


def sort_products_by_price(
    products: List[Product], reverse: bool = False
) -> List[Product]:
    """Отсортировать товары по цене."""
    return sorted(products, key=lambda prod: prod.price, reverse=reverse)


def show_products(products: List[Product]) -> None:
    """Вывести все товары."""
    print("\n--- Товары ---")
    if not products:
        print("Товары отсутствуют")
        return
    for product in products:
        print(f"  {product}")
