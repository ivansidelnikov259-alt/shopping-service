"""
Модуль подключения к базе данных SQLite.

Содержит:
- get_connection() — соединение с настройками row_factory и PRAGMA;
- execute_query() — выполнение произвольного запроса;
- execute_one() — получение одной записи.
"""

import sqlite3
from typing import Any, List, Optional

DB_PATH = "data/shopping_service.sqlite"


def get_connection() -> sqlite3.Connection:
    """
    Открыть соединение с базой данных.

    Returns:
        Соединение с включёнными внешними ключами и row_factory = Row.
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def execute_query(
    query: str,
    params: Optional[List[Any]] = None,
) -> List[sqlite3.Row]:
    """
    Выполнить SELECT-запрос и вернуть все строки.

    Args:
        query: SQL-запрос с заполнителями ?.
        params: Список параметров для подстановки.

    Returns:
        Список строк (sqlite3.Row).
    """
    conn = get_connection()
    try:
        cursor = conn.execute(query, params or [])
        rows = cursor.fetchall()
        return rows
    finally:
        conn.close()


def execute_one(
    query: str,
    params: Optional[List[Any]] = None,
) -> Optional[sqlite3.Row]:
    """
    Выполнить SELECT-запрос и вернуть одну строку.

    Args:
        query: SQL-запрос с заполнителями ?.
        params: Список параметров для подстановки.

    Returns:
        Одна строка (sqlite3.Row) или None.
    """
    conn = get_connection()
    try:
        cursor = conn.execute(query, params or [])
        return cursor.fetchone()
    finally:
        conn.close()
