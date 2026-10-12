SELECT
    order_id,
    customer_id,
    employee_id,
    store_id,
    order_date,
    order_status,
    payment_method,
    sales_channel,
    subtotal_amount,
    discount_amount,
    tax_amount,
    total_amount,
    created_at,
    updated_at
FROM read_parquet(
    's3://enterprise-sales/silver/orders/*.parquet'
)