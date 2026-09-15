"""
Вспомогательные функции для сервиса учёта покупок.
"""

from datetime import date


def input_int(prompt: str) -> int:
    """Запрашивает у пользователя целое число."""
    while True:
        try:
            return int(input(prompt).strip())
        except ValueError:
            print("Ошибка: введите целое число.")


def input_float(prompt: str) -> float:
    """Запрашивает у пользователя положительное число."""
    while True:
        try:
            value = float(input(prompt).strip())
            if value <= 0:
                print("Ошибка: число должно быть больше нуля.")
                continue
            return value
        except ValueError:
            print("Ошибка: введите корректное число.")


def input_date(prompt: str) -> date:
    """Запрашивает у пользователя дату."""
    while True:
        date_str = input(prompt).strip()
        if not date_str:
            return date.today()
        try:
            day, month, year = date_str.split(".")
            return date(int(year), int(month), int(day))
        except (ValueError, TypeError):
            print("Ошибка: неверный формат даты. Используйте ДД.ММ.ГГГГ")


def input_non_empty(prompt: str) -> str:
    """Запрашивает непустую строку."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Ошибка: значение не может быть пустым.")
