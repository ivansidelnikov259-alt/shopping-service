"""
Тесты SQL-слоя (SQLite).
"""

import sqlite3

import pytest

import db.database as database
from db.database import execute_one, execute_query, get_connection


@pytest.fixture
def temp_db(tmp_path, monkeypatch):
    """Создать временную БД с минимальной схемой."""
    db_path = tmp_path / "test.sqlite"
    monkeypatch.setattr(database, "DB_PATH", str(db_path))

    conn = sqlite3.connect(str(db_path))
    conn.executescript(
        """
        CREATE TABLE purchases (
            id INTEGER PRIMARY KEY,
            product_name TEXT,
            price REAL,
            category_name TEXT
        );
        INSERT INTO purchases VALUES (1, 'Молоко', 100.0, 'Продукты');
        INSERT INTO purchases VALUES (2, 'Хлеб', 50.0, 'Продукты');
        """
    )
    conn.commit()
    conn.close()
    return db_path


def test_get_connection_row_factory(temp_db):
    """Проверяет, что row_factory = Row."""
    conn = get_connection()
    assert conn.row_factory is sqlite3.Row
    conn.close()


def test_execute_query_returns_all(temp_db):
    """Проверяет получение всех записей."""
    rows = execute_query("SELECT * FROM purchases ORDER BY id")
    assert len(rows) == 2
    assert rows[0]["product_name"] == "Молоко"


def test_execute_one_returns_first(temp_db):
    """Проверяет получение одной записи."""
    row = execute_one(
        "SELECT * FROM purchases WHERE id = ?", [1]
    )
    assert row is not None
    assert row["product_name"] == "Молоко"


def test_execute_one_returns_none(temp_db):
    """Проверяет, что несуществующий ID даёт None."""
    row = execute_one("SELECT * FROM purchases WHERE id = ?", [999])
    assert row is None


def test_parametrized_query_prevents_injection(temp_db):
    """Проверяет параметризованный запрос."""
    pattern = "%олок%"
    rows = execute_query(
        "SELECT * FROM purchases WHERE product_name LIKE ?",
        [pattern],
    )
    assert len(rows) == 1
    assert rows[0]["product_name"] == "Молоко"
