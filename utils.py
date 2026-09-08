"""
Вспомогательные функции для сервиса учета покупок.
"""

from datetime import date


def input_int(prompt: str) -> int:
    """
    Запрашивает у пользователя целое число.

    Args:
        prompt: Текст приглашения для ввода.

    Returns:
        Введенное целое число.
    """
    while True:
        try:
            value = input(prompt).strip()
            return int(value)
        except ValueError:
            print("Ошибка: введите целое число.")


def input_float(prompt: str) -> float:
    """
    Запрашивает у пользователя число с плавающей точкой.

    Args:
        prompt: Текст приглашения для ввода.

    Returns:
        Введенное число.
    """
    while True:
        try:
            value = input(prompt).strip()
            result = float(value)
            if result <= 0:
                print("Ошибка: число должно быть больше нуля.")
                continue
            return result
        except ValueError:
            print("Ошибка: введите корректное число.")


def input_date(prompt: str) -> date:
    """
    Запрашивает у пользователя дату.

    Args:
        prompt: Текст приглашения для ввода.

    Returns:
        Объект date.
    """
    while True:
        date_str = input(prompt).strip()
        if not date_str:
            return date.today()

        try:
            day, month, year = date_str.split('.')
            return date(int(year), int(month), int(day))
        except (ValueError, TypeError):
            print("Ошибка: неверный формат даты. Используйте ДД.ММ.ГГГГ")


def input_non_empty(prompt: str) -> str:
    """
    Запрашивает у пользователя непустую строку.

    Args:
        prompt: Текст приглашения для ввода.

    Returns:
        Введенная строка.
    """
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Ошибка: значение не может быть пустым.")
