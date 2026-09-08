"""
Тесты для сервиса учета покупок.
"""

from storage import load_data, save_data
from utils import input_float, input_non_empty
from main import get_next_id


def test_get_next_id():
    """Тест функции получения следующего ID."""
    # Пустой список
    assert get_next_id([]) == 1

    # Список с элементами
    items = [{"id": 1}, {"id": 5}, {"id": 3}]
    assert get_next_id(items) == 6


def test_load_empty_data():
    """Тест загрузки несуществующего файла."""
    data = load_data("nonexistent_file.json")
    assert data == []


def test_save_and_load_data(tmp_path, monkeypatch):
    """Тест сохранения и загрузки данных."""
    import storage
    monkeypatch.setattr(storage, "DATA_DIR", tmp_path)

    test_data = [{"id": 1, "name": "Тест"}]

    # Сохраняем
    assert save_data("test.json", test_data) is True

    # Загружаем
    loaded = load_data("test.json")
    assert len(loaded) == 1
    assert loaded[0]["name"] == "Тест"


def test_input_float_validation(monkeypatch):
    """Тест валидации ввода числа."""
    # Имитируем ввод пользователя
    inputs = iter(["abc", "-5", "10.5"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    result = input_float("Введите число: ")
    assert result == 10.5


def test_input_non_empty(monkeypatch):
    """Тест ввода непустой строки."""
    inputs = iter(["", "  ", "Тест"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    result = input_non_empty("Введите строку: ")
    assert result == "Тест"


def test_add_purchase():
    """Тест добавления покупки."""
    purchases = []
    purchase = {
        "id": get_next_id(purchases),
        "product": "Молоко",
        "price": 89.90,
        "category": "Продукты",
        "store": "Пятёрочка",
        "date": "2026-09-08"
    }
    purchases.append(purchase)

    assert len(purchases) == 1
    assert purchases[0]["product"] == "Молоко"
    assert purchases[0]["price"] == 89.90
