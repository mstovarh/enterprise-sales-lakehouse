SET search_path TO erp;

-- =========================================================
-- Stores
-- =========================================================
INSERT INTO stores (
    store_name,
    city,
    region,
    channel,
    opened_at
)
VALUES
    ('NovaRetail Bogotá Centro', 'Bogotá', 'Andina', 'PHYSICAL', '2021-03-15'),
    ('NovaRetail Medellín', 'Medellín', 'Andina', 'PHYSICAL', '2022-07-10'),
    ('NovaRetail Online', 'Bogotá', 'Nacional', 'ONLINE', '2020-01-01');

-- =========================================================
-- Customers
-- =========================================================
INSERT INTO customers (
    first_name,
    last_name,
    email,
    phone,
    city,
    country,
    customer_segment
)
VALUES
    ('Laura', 'Martínez', 'laura.martinez@example.com', '3001112233', 'Bogotá', 'Colombia', 'PREMIUM'),
    ('Carlos', 'Gómez', 'carlos.gomez@example.com', '3012223344', 'Medellín', 'Colombia', 'REGULAR'),
    ('Andrea', 'Rodríguez', 'andrea.rodriguez@example.com', '3023334455', 'Barranquilla', 'Colombia', 'CORPORATE'),
    ('Miguel', 'Torres', 'miguel.torres@example.com', '3034445566', 'Cali', 'Colombia', 'REGULAR');

-- =========================================================
-- Employees
-- =========================================================
INSERT INTO employees (
    store_id,
    first_name,
    last_name,
    email,
    job_title,
    hire_date
)
VALUES
    (1, 'Sofía', 'Ramírez', 'sofia.ramirez@novaretail.com', 'Sales Advisor', '2023-01-10'),
    (2, 'Daniel', 'Pérez', 'daniel.perez@novaretail.com', 'Sales Advisor', '2023-05-20'),
    (3, 'Valentina', 'López', 'valentina.lopez@novaretail.com', 'E-commerce Specialist', '2022-09-01');

-- =========================================================
-- Products
-- =========================================================
INSERT INTO products (
    sku,
    product_name,
    category,
    brand,
    unit_cost,
    unit_price,
    stock_quantity
)
VALUES
    ('LAP-001', 'Laptop NovaBook 14', 'Computers', 'NovaTech', 1800000, 2499000, 25),
    ('PHO-001', 'Smartphone Nova X', 'Smartphones', 'NovaTech', 900000, 1399000, 60),
    ('TV-001', 'Smart TV 55 pulgadas', 'Televisions', 'VisionPlus', 1400000, 1999000, 18),
    ('ACC-001', 'Wireless Mouse', 'Accessories', 'ClickPro', 50000, 89900, 120),
    ('ACC-002', 'Mechanical Keyboard', 'Accessories', 'KeyMaster', 150000, 249900, 70);

-- =========================================================
-- Orders
-- =========================================================
INSERT INTO orders (
    customer_id,
    store_id,
    employee_id,
    order_date,
    order_status,
    payment_method,
    sales_channel,
    subtotal_amount,
    discount_amount,
    tax_amount,
    total_amount
)
VALUES
    (
        1, 1, 1,
        '2026-08-01 10:30:00',
        'COMPLETED',
        'CREDIT_CARD',
        'STORE',
        2589900,
        100000,
        473081,
        2962981
    ),
    (
        2, 2, 2,
        '2026-08-02 14:15:00',
        'COMPLETED',
        'PSE',
        'STORE',
        1399000,
        0,
        265810,
        1664810
    ),
    (
        3, 3, 3,
        '2026-08-03 09:00:00',
        'PAID',
        'TRANSFER',
        'WEB',
        2248900,
        50000,
        417791,
        2616691
    );

-- =========================================================
-- Order Items
-- =========================================================
INSERT INTO order_items (
    order_id,
    product_id,
    quantity,
    unit_price,
    discount_amount,
    line_total
)
VALUES
    (1, 1, 1, 2499000, 100000, 2399000),
    (1, 4, 1, 89900, 0, 89900),
    (2, 2, 1, 1399000, 0, 1399000),
    (3, 3, 1, 1999000, 50000, 1949000),
    (3, 5, 1, 249900, 0, 249900);
