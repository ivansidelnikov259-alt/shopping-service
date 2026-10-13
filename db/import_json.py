"""
Скрипт переноса данных из JSON-файлов в SQLite.

Запуск:
    python -m db.import_json
"""

import json
from pathlib import Path

from db.database import get_connection

DATA_DIR = Path("data")


def load_json(filename: str) -> list:
    """Загрузить JSON-файл."""
    filepath = DATA_DIR / filename
    if not filepath.exists():
        return []
    with open(filepath, "r", encoding="utf-8") as file:
        return json.load(file)


def import_users(conn) -> None:
    """Перенести пользователей в таблицу users (если файл есть)."""
    users = load_json("users.json")
    if not users:
        return
    conn.executemany(
        """
        INSERT OR REPLACE INTO users (id, name, email)
        VALUES (?, ?, ?)
        """,
        [
            (u["id"], u["name"], u.get("email", ""))
            for u in users
        ],
    )


def import_categories(conn) -> None:
    """Перенести категории в таблицу categories."""
    categories = load_json("categories.json")
    if not categories:
        return
    conn.executemany(
        """
        INSERT OR REPLACE INTO categories (id, name)
        VALUES (?, ?)
        """,
        [(c["id"], c["name"]) for c in categories],
    )


def import_stores(conn) -> None:
    """Перенести магазины в таблицу stores."""
    stores = load_json("stores.json")
    if not stores:
        return
    conn.executemany(
        """
        INSERT OR REPLACE INTO stores (id, name, address)
        VALUES (?, ?, ?)
        """,
        [
            (s["id"], s["name"], s.get("address", ""))
            for s in stores
        ],
    )


def import_purchases(conn) -> None:
    """Перенести покупки в таблицу purchases."""
    purchases = load_json("purchases.json")
    if not purchases:
        return
    conn.executemany(
        """
        INSERT OR REPLACE INTO purchases (
            id, product_id, product_name, price,
            category_id, category_name,
            store_id, store_name, purchase_date
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        [
            (
                p["id"],
                p.get("product_id", 0),
                p["product_name"],
                p["price"],
                p.get("category_id"),
                p["category_name"],
                p.get("store_id"),
                p["store_name"],
                p["date"],
            )
            for p in purchases
        ],
    )


def import_shopping_lists(conn) -> None:
    """Перенести списки покупок в shopping_lists + shopping_list_items."""
    lists = load_json("shopping_lists.json")
    if not lists:
        return

    lists_rows = [
        (
            sl["id"],
            sl["name"],
            sl["created_at"],
            int(sl.get("is_completed", False)),
        )
        for sl in lists
    ]
    conn.executemany(
        """
        INSERT OR REPLACE INTO shopping_lists (
            id, name, created_at, is_completed
        )
        VALUES (?, ?, ?, ?)
        """,
        lists_rows,
    )

    items_rows = []
    for sl in lists:
        for item in sl.get("items", []):
            items_rows.append(
                (
                    item["id"],
                    sl["id"],
                    item["name"],
                    item["price"],
                )
            )
    if items_rows:
        conn.executemany(
            """
            INSERT OR REPLACE INTO shopping_list_items (
                id, list_id, product_name, price
            )
            VALUES (?, ?, ?, ?)
            """,
            items_rows,
        )


def main() -> None:
    """Главная функция импорта."""
    conn = get_connection()
    try:
        import_users(conn)
        import_categories(conn)
        import_stores(conn)
        import_purchases(conn)
        import_shopping_lists(conn)
        conn.commit()
        print("Импорт завершён успешно.")
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    main()
