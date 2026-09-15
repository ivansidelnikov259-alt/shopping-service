"""
Модуль сущности «Пользователь».

Наследуется от BaseEntity.
"""

from typing import List, Optional

from .base import BaseEntity


class User(BaseEntity):
    """
    Пользователь системы.

    Дополнительный атрибут: _email.
    """

    def __init__(self, user_id: int, name: str, email: str) -> None:
        """Создать объект пользователя."""
        super().__init__(entity_id=user_id, name=name)
        self._email = email

    @property
    def email(self) -> str:
        """Email пользователя."""
        return self._email

    @email.setter
    def email(self, value: str) -> None:
        """Установить email с проверкой."""
        if not self._validate_email(value):
            raise ValueError(f"Некорректный email: {value}")
        self._email = value

    def __str__(self) -> str:
        """Строковое представление пользователя."""
        return f"Пользователь #{self.id}: {self.name} <{self.email}>"

    def to_dict(self) -> dict:
        """Преобразовать в словарь."""
        return {"id": self.id, "name": self.name, "email": self.email}

    @classmethod
    def from_data(cls, data: dict) -> "User":
        """Создать объект из словаря."""
        return cls(
            user_id=data["id"], name=data["name"], email=data["email"]
        )

    @staticmethod
    def _validate_email(email: str) -> bool:
        """Проверить корректность email."""
        return "@" in email and "." in email.split("@")[-1]

    def is_valid_email(self) -> bool:
        """Публичная проверка email."""
        return self._validate_email(self._email)


def get_next_id(users: List[User]) -> int:
    """Получить следующий свободный ID."""
    if not users:
        return 1
    return max(user.id for user in users) + 1


def add_user(users: List[User], name: str, email: str) -> User:
    """Создать нового пользователя."""
    new_id = get_next_id(users)
    user = User(user_id=new_id, name=name, email=email)
    users.append(user)
    return user


def find_user_by_id(users: List[User], user_id: int) -> Optional[User]:
    """Найти пользователя по ID."""
    for user in users:
        if user.id == user_id:
            return user
    return None


def find_user_by_email(users: List[User], email: str) -> Optional[User]:
    """Найти пользователя по email."""
    email_lower = email.lower()
    for user in users:
        if user.email.lower() == email_lower:
            return user
    return None


def show_users(users: List[User]) -> None:
    """Вывести всех пользователей."""
    print("\n--- Пользователи ---")
    if not users:
        print("Пользователи отсутствуют")
        return
    for user in users:
        print(f"  {user}")
