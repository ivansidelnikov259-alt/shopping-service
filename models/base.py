"""
Базовый класс для всех сущностей предметной области.

Демонстрирует принципы ООП:
- инкапсуляция (защищённые атрибуты _id, _name);
- наследование (все сущности наследуются от BaseEntity);
- полиморфизм (метод __str__ переопределяется в подклассах).
"""

from abc import ABC, abstractmethod


class BaseEntity(ABC):
    """
    Абстрактный базовый класс для всех сущностей.

    Атрибуты:
        _id: защищённый идентификатор.
        _name: защищённое название.

    Методы:
        id: свойство для чтения идентификатора.
        name: свойство для чтения/записи названия.
        to_dict: абстрактный метод сериализации.
        __str__: абстрактное строковое представление.
    """

    def __init__(self, entity_id: int, name: str) -> None:
        """
        Инициализировать базовую сущность.

        Args:
            entity_id: Уникальный идентификатор.
            name: Название сущности.
        """
        self._id = entity_id
        self._name = name

    @property
    def id(self) -> int:
        """Уникальный идентификатор (только для чтения)."""
        return self._id

    @property
    def name(self) -> str:
        """Название сущности."""
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        """
        Установить название.

        Args:
            value: Новое название.

        Raises:
            ValueError: Если название пустое.
        """
        if not value or not value.strip():
            raise ValueError("Название не может быть пустым")
        self._name = value.strip()

    @abstractmethod
    def to_dict(self) -> dict:
        """Сериализовать объект в словарь для JSON."""
        ...

    @abstractmethod
    def __str__(self) -> str:
        """Строковое представление объекта."""
        ...

    def __repr__(self) -> str:
        """Техническое представление для отладки."""
        return f"{self.__class__.__name__}(id={self._id}, name={self._name!r})"

    def __eq__(self, other: object) -> bool:
        """Сравнение объектов по классу и ID."""
        if not isinstance(other, BaseEntity):
            return NotImplemented
        return self.__class__ is other.__class__ and self._id == other._id

    def __hash__(self) -> int:
        """Хеш по ID — позволяет использовать объекты в set и dict."""
        return hash((self.__class__.__name__, self._id))
