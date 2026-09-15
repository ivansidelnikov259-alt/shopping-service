"""
Модуль сущности «Категория».

Наследуется от BaseEntity.
"""

from typing import List, Optional

from .base import BaseEntity


class Category(BaseEntity):
    """
    Категория товаров.

    Наследует атрибуты _id, _name от BaseEntity.
    """

    def __init__(self, category_id: int, name: str) -> None:
        """Создать объект категории."""
        super().__init__(entity_id=category_id, name=name)

    def __str__(self) -> str:
        """Строковое представление категории."""
        return f"Категория #{self.id}: {self.name}"

    def to_dict(self) -> dict:
        """Преобразовать в словарь для JSON."""
        return {"id": self.id, "name": self.name}

    @classmethod
    def from_data(cls, data: dict) -> "Category":
        """Создать объект из словаря."""
        return cls(category_id=data["id"], name=data["name"])

    @staticmethod
    def validate_name(name: str) -> bool:
        """
        Проверить корректность названия категории.

        Args:
            name: Название для проверки.

        Returns:
            True, если название корректно.
        """
        return bool(name and name.strip())


def get_next_id(categories: List[Category]) -> int:
    """Получить следующий свободный ID."""
    if not categories:
        return 1
    return max(cat.id for cat in categories) + 1


def add_category(categories: List[Category], name: str) -> Category:
    """Создать новую категорию и добавить её в коллекцию."""
    if not Category.validate_name(name):
        raise ValueError("Некорректное название категории")
    new_id = get_next_id(categories)
    category = Category(category_id=new_id, name=name.strip())
    categories.append(category)
    return category


def find_category_by_id(
    categories: List[Category], category_id: int
) -> Optional[Category]:
    """Найти категорию по ID."""
    for category in categories:
        if category.id == category_id:
            return category
    return None


def find_category_by_name(
    categories: List[Category], name: str
) -> Optional[Category]:
    """Найти категорию по названию (без учёта регистра)."""
    name_lower = name.lower()
    for category in categories:
        if category.name.lower() == name_lower:
            return category
    return None


def get_or_create_category(categories: List[Category], name: str) -> Category:
    """Найти категорию по имени или создать новую."""
    existing = find_category_by_name(categories, name)
    if existing is not None:
        return existing
    return add_category(categories, name)


def show_categories(categories: List[Category]) -> None:
    """Вывести все категории."""
    print("\n--- Категории ---")
    if not categories:
        print("Категории отсутствуют")
        return
    for category in categories:
        print(f"  {category}")
