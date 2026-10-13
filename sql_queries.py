"""
SQL-запросы, используемые в Django-представлениях.

Дублируют sql/queries.sql — так удобнее импортировать их в Python-код.
"""

# Список покупок
PURCHASES_LIST = """
SELECT
    id, product_name, price,
    category_name, store_name, purchase_date
FROM purchases
ORDER BY purchase_date DESC
"""

# Общая сумма покупок
PURCHASES_TOTAL_SUM = """
SELECT SUM(price) AS total_sum FROM purchases
"""

# Одна покупка по ID
PURCHASE_BY_ID = """
SELECT
    id, product_name, price,
    category_name, store_name, purchase_date
FROM purchases
WHERE id = ?
"""

# Поиск покупок по названию (параметризованный)
PURCHASE_SEARCH = """
SELECT
    id, product_name, price,
    category_name, store_name, purchase_date
FROM purchases
WHERE product_name LIKE ?
ORDER BY purchase_date DESC
"""

# Статистика: количество и сумма по категориям
PURCHASES_STATISTICS = """
SELECT
    category_name,
    COUNT(*) AS purchases_count,
    SUM(price) AS total_sum
FROM purchases
GROUP BY category_name
ORDER BY total_sum DESC
"""

# Покупки по категории (WHERE)
PURCHASES_BY_CATEGORY = """
SELECT
    id, product_name, price, purchase_date
FROM purchases
WHERE category_name = 'Продукты'
ORDER BY purchase_date DESC
"""
