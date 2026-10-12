WITH order_items AS (

    SELECT *
    FROM read_parquet(
        's3://enterprise-sales/silver/order_items/*.parquet'
    )

),

orders AS (

    SELECT *
    FROM {{ ref('stg_orders') }}

),

products AS (

    SELECT *
    FROM read_parquet(
        's3://enterprise-sales/silver/products/*.parquet'
    )

),

customers AS (

    SELECT *
    FROM read_parquet(
        's3://enterprise-sales/silver/customers/*.parquet'
    )

),

stores AS (

    SELECT *
    FROM read_parquet(
        's3://enterprise-sales/silver/stores/*.parquet'
    )

)

SELECT
    oi.order_item_id,
    oi.order_id,

    o.order_date,
    o.order_status,
    o.payment_method,
    o.sales_channel,

    oi.product_id,
    p.product_name,
    p.category,
    p.brand,

    o.customer_id,
    CONCAT(c.first_name, ' ', c.last_name) AS customer_name,
    c.customer_segment,

    o.store_id,
    s.store_name,
    s.city AS store_city,
    s.region,

    oi.quantity,
    oi.unit_price,
    oi.discount_amount,
    oi.line_total,

    o.subtotal_amount,
    o.tax_amount,
    o.total_amount

FROM order_items oi

INNER JOIN orders o
    ON oi.order_id = o.order_id

LEFT JOIN products p
    ON oi.product_id = p.product_id

LEFT JOIN customers c
    ON o.customer_id = c.customer_id

LEFT JOIN stores s
    ON o.store_id = s.store_id