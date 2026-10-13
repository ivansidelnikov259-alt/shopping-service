"""
SQL-запросы для приложения shopping_lists.
"""

# Все списки с подсчётом товаров
LISTS_ALL = """
SELECT
    shopping_lists.id,
    shopping_lists.name,
    shopping_lists.created_at,
    shopping_lists.is_completed,
    COUNT(shopping_list_items.id) AS items_count
FROM shopping_lists
LEFT JOIN shopping_list_items
    ON shopping_lists.id = shopping_list_items.list_id
GROUP BY shopping_lists.id
ORDER BY shopping_lists.name
"""

# Один список по ID
LIST_BY_ID = """
SELECT
    id, name, created_at, is_completed
FROM shopping_lists
WHERE id = ?
"""

# Товары списка (JOIN)
LIST_ITEMS = """
SELECT
    id, product_name, price
FROM shopping_list_items
WHERE list_id = ?
ORDER BY id
"""

# Поиск списков по названию (параметризованный)
LIST_SEARCH = """
SELECT id, name, created_at, is_completed
FROM shopping_lists
WHERE name LIKE ?
ORDER BY name
"""
