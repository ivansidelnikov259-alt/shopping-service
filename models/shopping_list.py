"""
Модуль сущности «Список покупок».

Наследуется от BaseEntity.
"""

from datetime import date
from typing import List, Optional

from .base import BaseEntity
from .product import Product


class ShoppingList(BaseEntity):
    """
    Список покупок.

    Дополнительные атрибуты:
        _items, _created_at, _is_completed.
    """

    def __init__(
        self,
        list_id: int,
        name: str,
        items: Optional[List[Product]] = None,
        created_at: Optional[date] = None,
        is_completed: bool = False,
    ) -> None:
        """Создать объект списка."""
        super().__init__(entity_id=list_id, name=name)
        self._items = items if items is not None else []
        self._created_at = created_at if created_at is not None else date.today()
        self._is_completed = is_completed

    @property
    def items(self) -> List[Product]:
        """Товары списка."""
        return self._items

    @property
    def created_at(self) -> date:
        """Дата создания."""
        return self._created_at

    @property
    def is_completed(self) -> bool:
        """Завершён ли список."""
        return self._is_completed

    @property
    def total(self) -> float:
        """Общая стоимость списка (вычисляемое свойство)."""
        return sum(p.price for p in self._items)

    def __str__(self) -> str:
        """Строковое представление списка."""
        status = "завершён" if self._is_completed else "активен"
        return (
            f"Список #{self.id}: {self.name} "
            f"({len(self._items)} товаров, {status}, "
            f"создан {self._created_at.strftime('%d.%m.%Y')})"
        )

    def add_item(self, product: Product) -> None:
        """Добавить товар."""
        self._items.append(product)

    def remove_item(self, product_id: int) -> bool:
        """Удалить товар по ID."""
        for i, product in enumerate(self._items):
            if product.id == product_id:
                self._items.pop(i)
                return True
        return False

    def complete(self) -> None:
        """Отметить как завершённый."""
        self._is_completed = True

    def to_dict(self) -> dict:
        """Преобразовать в словарь."""
        return {
            "id": self.id,
            "name": self.name,
            "items": [p.to_dict() for p in self._items],
            "created_at": self._created_at.isoformat(),
            "is_completed": self._is_completed,
        }

    @classmethod
    def from_data(cls, data: dict) -> "ShoppingList":
        """Создать объект из словаря."""
        items = [
            Product.from_data(item, []) for item in data.get("items", [])
        ]
        created_at = date.fromisoformat(data["created_at"])
        return cls(
            list_id=data["id"],
            name=data["name"],
            items=items,
            created_at=created_at,
            is_completed=data.get("is_completed", False),
        )


def get_next_id(shopping_lists: List[ShoppingList]) -> int:
    """Следующий свободный ID."""
    if not shopping_lists:
        return 1
    return max(sl.id for sl in shopping_lists) + 1


def add_shopping_list(
    shopping_lists: List[ShoppingList], name: str
) -> ShoppingList:
    """Создать новый список."""
    new_id = get_next_id(shopping_lists)
    shopping_list = ShoppingList(list_id=new_id, name=name)
    shopping_lists.append(shopping_list)
    return shopping_list


def find_shopping_list_by_id(
    shopping_lists: List[ShoppingList], list_id: int
) -> Optional[ShoppingList]:
    """Найти список по ID."""
    for sl in shopping_lists:
        if sl.id == list_id:
            return sl
    return None


def delete_shopping_list(
    shopping_lists: List[ShoppingList], list_id: int
) -> bool:
    """Удалить список по ID."""
    for i, sl in enumerate(shopping_lists):
        if sl.id == list_id:
            shopping_lists.pop(i)
            return True
    return False


def show_shopping_lists(shopping_lists: List[ShoppingList]) -> None:
    """Вывести все списки."""
    print("\n--- Списки покупок ---")
    if not shopping_lists:
        print("Списки отсутствуют")
        return
    for sl in shopping_lists:
        print(f"\n  {sl}")
        for product in sl.items:
            print(f"    - {product}")
        if sl.items:
            print(f"    Итого: {sl.total:.2f} руб.")
