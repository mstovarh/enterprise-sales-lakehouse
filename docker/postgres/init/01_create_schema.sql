-- =========================================================
-- NovaRetail ERP - Transactional Source Schema
-- =========================================================

CREATE SCHEMA IF NOT EXISTS erp;

SET search_path TO erp;

-- =========================================================
-- Customers
-- =========================================================
CREATE TABLE IF NOT EXISTS customers (
    customer_id       BIGSERIAL PRIMARY KEY,
    first_name        VARCHAR(80) NOT NULL,
    last_name         VARCHAR(80) NOT NULL,
    email             VARCHAR(150) NOT NULL UNIQUE,
    phone             VARCHAR(30),
    city              VARCHAR(100) NOT NULL,
    country           VARCHAR(100) NOT NULL DEFAULT 'Colombia',
    customer_segment  VARCHAR(30) NOT NULL DEFAULT 'REGULAR',
    created_at        TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at        TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT chk_customer_segment
        CHECK (customer_segment IN ('REGULAR', 'PREMIUM', 'CORPORATE'))
);

-- =========================================================
-- Stores
-- =========================================================
CREATE TABLE IF NOT EXISTS stores (
    store_id      BIGSERIAL PRIMARY KEY,
    store_name    VARCHAR(120) NOT NULL,
    city          VARCHAR(100) NOT NULL,
    region        VARCHAR(100) NOT NULL,
    channel       VARCHAR(30) NOT NULL,
    opened_at     DATE,
    is_active     BOOLEAN NOT NULL DEFAULT TRUE,

    CONSTRAINT chk_store_channel
        CHECK (channel IN ('PHYSICAL', 'ONLINE', 'MARKETPLACE'))
);

-- =========================================================
-- Employees
-- =========================================================
CREATE TABLE IF NOT EXISTS employees (
    employee_id    BIGSERIAL PRIMARY KEY,
    store_id       BIGINT NOT NULL,
    first_name     VARCHAR(80) NOT NULL,
    last_name      VARCHAR(80) NOT NULL,
    email          VARCHAR(150) NOT NULL UNIQUE,
    job_title      VARCHAR(80) NOT NULL,
    hire_date      DATE NOT NULL,
    is_active      BOOLEAN NOT NULL DEFAULT TRUE,

    CONSTRAINT fk_employees_store
        FOREIGN KEY (store_id)
        REFERENCES stores(store_id)
);

-- =========================================================
-- Products
-- =========================================================
CREATE TABLE IF NOT EXISTS products (
    product_id      BIGSERIAL PRIMARY KEY,
    sku             VARCHAR(50) NOT NULL UNIQUE,
    product_name    VARCHAR(150) NOT NULL,
    category        VARCHAR(80) NOT NULL,
    brand           VARCHAR(80) NOT NULL,
    unit_cost       NUMERIC(12,2) NOT NULL,
    unit_price      NUMERIC(12,2) NOT NULL,
    stock_quantity  INTEGER NOT NULL DEFAULT 0,
    is_active       BOOLEAN NOT NULL DEFAULT TRUE,
    created_at      TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT chk_product_cost
        CHECK (unit_cost >= 0),

    CONSTRAINT chk_product_price
        CHECK (unit_price > 0),

    CONSTRAINT chk_product_stock
        CHECK (stock_quantity >= 0)
);

-- =========================================================
-- Orders
-- =========================================================
CREATE TABLE IF NOT EXISTS orders (
    order_id          BIGSERIAL PRIMARY KEY,
    customer_id       BIGINT NOT NULL,
    store_id          BIGINT NOT NULL,
    employee_id       BIGINT,
    order_date        TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    order_status      VARCHAR(30) NOT NULL,
    payment_method    VARCHAR(30) NOT NULL,
    sales_channel     VARCHAR(30) NOT NULL,
    subtotal_amount   NUMERIC(14,2) NOT NULL DEFAULT 0,
    discount_amount   NUMERIC(14,2) NOT NULL DEFAULT 0,
    tax_amount        NUMERIC(14,2) NOT NULL DEFAULT 0,
    total_amount      NUMERIC(14,2) NOT NULL DEFAULT 0,
    created_at        TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at        TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_orders_customer
        FOREIGN KEY (customer_id)
        REFERENCES customers(customer_id),

    CONSTRAINT fk_orders_store
        FOREIGN KEY (store_id)
        REFERENCES stores(store_id),

    CONSTRAINT fk_orders_employee
        FOREIGN KEY (employee_id)
        REFERENCES employees(employee_id),

    CONSTRAINT chk_order_status
        CHECK (
            order_status IN (
                'CREATED',
                'PAID',
                'SHIPPED',
                'COMPLETED',
                'CANCELLED',
                'REFUNDED'
            )
        ),

    CONSTRAINT chk_payment_method
        CHECK (
            payment_method IN (
                'CASH',
                'CREDIT_CARD',
                'DEBIT_CARD',
                'TRANSFER',
                'PSE'
            )
        ),

    CONSTRAINT chk_sales_channel
        CHECK (
            sales_channel IN (
                'STORE',
                'WEB',
                'MOBILE',
                'MARKETPLACE'
            )
        ),

    CONSTRAINT chk_order_amounts
        CHECK (
            subtotal_amount >= 0
            AND discount_amount >= 0
            AND tax_amount >= 0
            AND total_amount >= 0
        )
);

-- =========================================================
-- Order Items
-- =========================================================
CREATE TABLE IF NOT EXISTS order_items (
    order_item_id   BIGSERIAL PRIMARY KEY,
    order_id        BIGINT NOT NULL,
    product_id      BIGINT NOT NULL,
    quantity        INTEGER NOT NULL,
    unit_price      NUMERIC(12,2) NOT NULL,
    discount_amount NUMERIC(12,2) NOT NULL DEFAULT 0,
    line_total      NUMERIC(14,2) NOT NULL,

    CONSTRAINT fk_order_items_order
        FOREIGN KEY (order_id)
        REFERENCES orders(order_id)
        ON DELETE CASCADE,

    CONSTRAINT fk_order_items_product
        FOREIGN KEY (product_id)
        REFERENCES products(product_id),

    CONSTRAINT chk_order_item_quantity
        CHECK (quantity > 0),

    CONSTRAINT chk_order_item_price
        CHECK (unit_price > 0),

    CONSTRAINT chk_order_item_discount
        CHECK (discount_amount >= 0),

    CONSTRAINT chk_order_item_total
        CHECK (line_total >= 0),

    CONSTRAINT uq_order_product
        UNIQUE (order_id, product_id)
);

-- =========================================================
-- Useful indexes
-- =========================================================
CREATE INDEX IF NOT EXISTS idx_orders_order_date
    ON orders(order_date);

CREATE INDEX IF NOT EXISTS idx_orders_customer_id
    ON orders(customer_id);

CREATE INDEX IF NOT EXISTS idx_orders_store_id
    ON orders(store_id);

CREATE INDEX IF NOT EXISTS idx_order_items_order_id
    ON order_items(order_id);

CREATE INDEX IF NOT EXISTS idx_order_items_product_id
    ON order_items(product_id);