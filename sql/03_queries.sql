SET search_path TO erp;

-- 1. Ver clientes
SELECT *
FROM customers
ORDER BY customer_id;

-- 2. Ver productos
SELECT *
FROM products
ORDER BY product_id;

-- 3. Ver órdenes con cliente y tienda
SELECT
    o.order_id,
    o.order_date,
    CONCAT(c.first_name, ' ', c.last_name) AS customer_name,
    s.store_name,
    o.sales_channel,
    o.order_status,
    o.total_amount
FROM orders o
INNER JOIN customers c
    ON c.customer_id = o.customer_id
INNER JOIN stores s
    ON s.store_id = o.store_id
ORDER BY o.order_date;

-- 4. Ver detalle de las ventas
SELECT
    o.order_id,
    o.order_date,
    p.sku,
    p.product_name,
    oi.quantity,
    oi.unit_price,
    oi.discount_amount,
    oi.line_total
FROM order_items oi
INNER JOIN orders o
    ON o.order_id = oi.order_id
INNER JOIN products p
    ON p.product_id = oi.product_id
ORDER BY o.order_id, oi.order_item_id;

-- 5. Ventas por ciudad del cliente
SELECT
    c.city,
    COUNT(DISTINCT o.order_id) AS total_orders,
    SUM(o.total_amount) AS total_sales
FROM orders o
INNER JOIN customers c
    ON c.customer_id = o.customer_id
GROUP BY c.city
ORDER BY total_sales DESC;

-- 6. Productos con mayores ingresos
SELECT
    p.product_name,
    SUM(oi.quantity) AS units_sold,
    SUM(oi.line_total) AS sales_amount
FROM order_items oi
INNER JOIN products p
    ON p.product_id = oi.product_id
GROUP BY p.product_id, p.product_name
ORDER BY sales_amount DESC;