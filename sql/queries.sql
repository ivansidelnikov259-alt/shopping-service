-- =============================================
-- Shopping Service: SQL-запросы проекта
-- =============================================
-- Минимум: 2×SELECT, 2×WHERE, 2×JOIN, 2×агрегат, 2×GROUP BY,
--          1×HAVING, 1×параметризованный
-- =============================================


-- ---------- SELECT: список покупок ----------
-- Все покупки с сортировкой по дате
SELECT id, product_name, price, purchase_date
FROM purchases
ORDER BY purchase_date DESC;


-- ---------- SELECT: список магазинов ----------
-- Все магазины с сортировкой по названию
SELECT id, name, address
FROM stores
ORDER BY name;


-- ---------- WHERE: покупки по категории ----------
-- Покупки в категории "Продукты"
SELECT id, product_name, price, purchase_date
FROM purchases
WHERE category_name = 'Продукты'
ORDER BY purchase_date DESC;


-- ---------- WHERE: дорогие товары ----------
-- Товары дороже 100 рублей
SELECT id, name, price
FROM products
WHERE price > 100
ORDER BY price DESC;


-- ---------- JOIN: полная информация о покупке ----------
-- Покупка + магазин + категория (через денормализованные поля)
SELECT
    purchases.id,
    purchases.product_name,
    purchases.price,
    purchases.category_name,
    purchases.store_name,
    purchases.purchase_date
FROM purchases
ORDER BY purchases.purchase_date DESC;


-- ---------- JOIN: списки с товарами ----------
-- Список покупок + все его товары
SELECT
    shopping_lists.name AS list_name,
    shopping_list_items.product_name,
    shopping_list_items.price
FROM shopping_lists
JOIN shopping_list_items
    ON shopping_lists.id = shopping_list_items.list_id
ORDER BY shopping_lists.name, shopping_list_items.id;


-- ---------- Агрегат: количество покупок ----------
SELECT COUNT(*) AS purchases_count
FROM purchases;


-- ---------- Агрегат: общая сумма покупок ----------
SELECT SUM(price) AS total_sum
FROM purchases;


-- ---------- GROUP BY: сумма по категориям ----------
SELECT
    category_name,
    COUNT(*) AS purchases_count,
    SUM(price) AS total_sum
FROM purchases
GROUP BY category_name
ORDER BY total_sum DESC;


-- ---------- GROUP BY: количество покупок по магазинам ----------
SELECT
    store_name,
    COUNT(*) AS purchases_count
FROM purchases
GROUP BY store_name
ORDER BY purchases_count DESC;


-- ---------- HAVING: категории с суммой больше порога ----------
SELECT
    category_name,
    SUM(price) AS total_sum
FROM purchases
GROUP BY category_name
HAVING SUM(price) > 100
ORDER BY total_sum DESC;


-- ---------- Параметризованный запрос: поиск покупок ----------
-- Значение передаётся через ? (см. db/database.py)
SELECT id, product_name, price, purchase_date
FROM purchases
WHERE product_name LIKE ?
ORDER BY purchase_date DESC;
