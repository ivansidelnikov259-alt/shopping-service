"""
Модуль сущности «Магазин».

Наследуется от BaseEntity.
"""

from typing import List, Optional

from .base import BaseEntity


class Store(BaseEntity):
    """
    Магазин — торговая точка.

    Дополнительный атрибут: _address.
    """

    def __init__(self, store_id: int, name: str, address: str = "") -> None:
        """Создать объект магазина."""
        super().__init__(entity_id=store_id, name=name)
        self._address = address

    @property
    def address(self) -> str:
        """Адрес магазина."""
        return self._address

    @address.setter
    def address(self, value: str) -> None:
        """Установить адрес магазина."""
        self._address = value.strip() if value else ""

    def __str__(self) -> str:
        """Строковое представление магазина."""
        if self.address:
            return f"Магазин #{self.id}: {self.name} ({self.address})"
        return f"Магазин #{self.id}: {self.name}"

    def to_dict(self) -> dict:
        """Преобразовать в словарь для JSON."""
        return {"id": self.id, "name": self.name, "address": self.address}

    @classmethod
    def from_data(cls, data: dict) -> "Store":
        """Создать объект из словаря."""
        return cls(
            store_id=data["id"],
            name=data["name"],
            address=data.get("address", ""),
        )


def get_next_id(stores: List[Store]) -> int:
    """Получить следующий свободный ID."""
    if not stores:
        return 1
    return max(store.id for store in stores) + 1


def add_store(stores: List[Store], name: str, address: str = "") -> Store:
    """Создать новый магазин."""
    new_id = get_next_id(stores)
    store = Store(store_id=new_id, name=name, address=address)
    stores.append(store)
    return store


def find_store_by_id(stores: List[Store], store_id: int) -> Optional[Store]:
    """Найти магазин по ID."""
    for store in stores:
        if store.id == store_id:
            return store
    return None


def find_store_by_name(stores: List[Store], name: str) -> Optional[Store]:
    """Найти магазин по имени."""
    name_lower = name.lower()
    for store in stores:
        if store.name.lower() == name_lower:
            return store
    return None


def get_or_create_store(stores: List[Store], name: str) -> Store:
    """Найти магазин по имени или создать новый."""
    existing = find_store_by_name(stores, name)
    if existing is not None:
        return existing
    return add_store(stores, name)


def show_stores(stores: List[Store]) -> None:
    """Вывести все магазины."""
    print("\n--- Магазины ---")
    if not stores:
        print("Магазины отсутствуют")
        return
    for store in stores:
        print(f"  {store}")
