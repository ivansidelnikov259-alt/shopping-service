"""
Модуль сущности «Покупка».

Наследуется от BaseEntity.
"""

from datetime import date
from typing import List, Optional

from .base import BaseEntity
from .category import Category
from .product import Product
from .store import Store


class Purchase(BaseEntity):
    """
    Покупка — запись о совершённой покупке.

    Дополнительные атрибуты:
        _product, _price, _category, _store, _purchase_date.
    """

    def __init__(
        self,
        purchase_id: int,
        product: Product,
        price: float,
        category: Category,
        store: Store,
        purchase_date: date,
    ) -> None:
        """Создать объект покупки."""
        super().__init__(entity_id=purchase_id, name=product.name)
        self._product = product
        self._price = price
        self._category = category
        self._store = store
        self._purchase_date = purchase_date

    @property
    def product(self) -> Product:
        """Товар покупки."""
        return self._product

    @property
    def price(self) -> float:
        """Цена покупки."""
        return self._price

    @property
    def category(self) -> Category:
        """Категория покупки."""
        return self._category

    @property
    def store(self) -> Store:
        """Магазин покупки."""
        return self._store

    @property
    def purchase_date(self) -> date:
        """Дата покупки."""
        return self._purchase_date

    @property
    def display_date(self) -> str:
        """Дата в формате ДД.ММ.ГГГГ (вычисляемое свойство)."""
        return self._purchase_date.strftime("%d.%m.%Y")

    def __str__(self) -> str:
        """Строковое представление покупки."""
        return (
            f"Покупка #{self.id}: {self.product.name} — "
            f"{self.price:.2f} руб. "
            f"(категория: {self.category.name}, "
            f"магазин: {self.store.name}, "
            f"дата: {self.display_date})"
        )

    def to_dict(self) -> dict:
        """Преобразовать в словарь."""
        return {
            "id": self.id,
            "product_id": self.product.id,
            "product_name": self.product.name,
            "price": self.price,
            "category_id": self.category.id,
            "category_name": self.category.name,
            "store_id": self.store.id,
            "store_name": self.store.name,
            "date": self.purchase_date.isoformat(),
        }

    @classmethod
    def from_data(cls, data: dict) -> "Purchase":
        """Создать объект из словаря."""
        product = Product(
            product_id=data["product_id"],
            name=data["product_name"],
            price=data["price"],
        )
        category = Category(
            category_id=data["category_id"], name=data["category_name"]
        )
        store = Store(
            store_id=data["store_id"], name=data["store_name"]
        )
        purchase_date = date.fromisoformat(data["date"])
        return cls(
            purchase_id=data["id"],
            product=product,
            price=data["price"],
            category=category,
            store=store,
            purchase_date=purchase_date,
        )


def get_next_id(purchases: List[Purchase]) -> int:
    """Получить следующий свободный ID."""
    if not purchases:
        return 1
    return max(p.id for p in purchases) + 1


def add_purchase(
    purchases: List[Purchase],
    product: Product,
    price: float,
    category: Category,
    store: Store,
    purchase_date: date,
) -> Purchase:
    """Создать новую покупку."""
    new_id = get_next_id(purchases)
    purchase = Purchase(
        purchase_id=new_id,
        product=product,
        price=price,
        category=category,
        store=store,
        purchase_date=purchase_date,
    )
    purchases.append(purchase)
    return purchase


def find_purchase_by_id(
    purchases: List[Purchase], purchase_id: int
) -> Optional[Purchase]:
    """Найти покупку по ID."""
    for p in purchases:
        if p.id == purchase_id:
            return p
    return None


def find_purchases_by_name(
    purchases: List[Purchase], query: str
) -> List[Purchase]:
    """Найти покупки по названию товара."""
    q = query.lower()
    return [p for p in purchases if q in p.product.name.lower()]


def delete_purchase(purchases: List[Purchase], purchase_id: int) -> bool:
    """Удалить покупку по ID."""
    for i, p in enumerate(purchases):
        if p.id == purchase_id:
            purchases.pop(i)
            return True
    return False


def get_total_sum(purchases: List[Purchase]) -> float:
    """Общая сумма покупок."""
    return sum(p.price for p in purchases)


def get_categories_summary(purchases: List[Purchase]) -> dict:
    """Суммы по категориям."""
    summary: dict = {}
    for p in purchases:
        name = p.category.name
        summary[name] = summary.get(name, 0.0) + p.price
    return summary


def show_purchases(purchases: List[Purchase]) -> None:
    """Вывести все покупки."""
    print("\n--- Все покупки ---")
    if not purchases:
        print("Покупки отсутствуют")
        return
    for p in purchases:
        print(f"  {p}")
    print(f"\nВсего покупок: {len(purchases)}")
    print(f"Общая сумма: {get_total_sum(purchases):.2f} руб.")
