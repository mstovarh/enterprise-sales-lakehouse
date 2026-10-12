SELECT
    store_id,
    store_name,
    store_city,
    region,

    COUNT(DISTINCT order_id) AS total_orders,

    SUM(quantity) AS total_units,

    SUM(CAST(line_total AS DECIMAL(18,2))) AS total_sales,

    AVG(CAST(line_total AS DECIMAL(18,2))) AS average_line_sales

FROM {{ ref('fct_sales') }}

GROUP BY
    store_id,
    store_name,
    store_city,
    region