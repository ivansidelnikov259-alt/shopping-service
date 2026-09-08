"""
Модуль для работы с файловым хранилищем данных.
"""

import json
from pathlib import Path
from typing import List

# Путь к папке с данными
DATA_DIR = Path("data")


def ensure_data_dir() -> None:
    """Создает папку для данных, если она не существует."""
    DATA_DIR.mkdir(exist_ok=True)


def load_data(filename: str) -> List[dict]:
    """
    Загружает данные из JSON файла.

    Args:
        filename: Имя файла.

    Returns:
        Список словарей с данными.
    """
    filepath = DATA_DIR / filename

    if not filepath.exists():
        return []

    try:
        with open(filepath, "r", encoding="utf-8") as file:
            data = json.load(file)
            if isinstance(data, list):
                return data
            return []
    except (json.JSONDecodeError, OSError):
        return []


def save_data(filename: str, data: List[dict]) -> bool:
    """
    Сохраняет данные в JSON файл.

    Args:
        filename: Имя файла.
        data: Список словарей для сохранения.

    Returns:
        True, если сохранение успешно.
    """
    ensure_data_dir()
    filepath = DATA_DIR / filename

    try:
        with open(filepath, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2, default=str)
        return True
    except OSError:
        return False
