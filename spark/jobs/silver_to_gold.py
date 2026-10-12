from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_timestamp
from pyspark.sql.types import DecimalType


# ============================================================
# Spark Session
# ============================================================

spark = (
    SparkSession.builder
    .appName("SilverToGold")
    .config("spark.hadoop.fs.s3a.endpoint", "http://minio:9000")
    .config("spark.hadoop.fs.s3a.access.key", "admin")
    .config("spark.hadoop.fs.s3a.secret.key", "admin123")
    .config("spark.hadoop.fs.s3a.path.style.access", "true")
    .config(
        "spark.hadoop.fs.s3a.impl",
        "org.apache.hadoop.fs.s3a.S3AFileSystem"
    )
    .config("spark.hadoop.fs.s3a.connection.ssl.enabled", "false")
    .getOrCreate()
)


# ============================================================
# Configuración
# ============================================================

BUCKET = "enterprise-sales"


def silver(table):
    return f"s3a://{BUCKET}/silver/{table}"


# ============================================================
# Leer Silver
# ============================================================

customers = spark.read.parquet(silver("customers"))
products = spark.read.parquet(silver("products"))
stores = spark.read.parquet(silver("stores"))
orders = spark.read.parquet(silver("orders"))
order_items = spark.read.parquet(silver("order_items"))


print("=== REGISTROS SILVER ===")
print(f"customers: {customers.count()}")
print(f"products: {products.count()}")
print(f"stores: {stores.count()}")
print(f"orders: {orders.count()}")
print(f"order_items: {order_items.count()}")


# ============================================================
# Preparar dimensiones
# ============================================================

customers = customers.select(
    "customer_id",
    "first_name",
    "last_name",
    "customer_segment",
    "city",
    "country"
)

products = products.select(
    "product_id",
    "sku",
    "product_name",
    "category",
    "brand",
    "unit_cost",
    "unit_price"
)

stores = stores.select(
    "store_id",
    "store_name",
    "city",
    "region",
    "channel"
)


# ============================================================
# Construir Gold Sales
# ============================================================

gold_sales = (
    order_items.alias("oi")

    .join(
        orders.alias("o"),
        col("oi.order_id") == col("o.order_id"),
        "inner"
    )

    .join(
        customers.alias("c"),
        col("o.customer_id") == col("c.customer_id"),
        "left"
    )

    .join(
        products.alias("p"),
        col("oi.product_id") == col("p.product_id"),
        "left"
    )

    .join(
        stores.alias("s"),
        col("o.store_id") == col("s.store_id"),
        "left"
    )

    .select(
        col("o.order_id"),

        # Fecha tipada
        to_timestamp(
            col("o.order_date")
        ).alias("order_date"),

        col("c.customer_id"),
        col("c.first_name"),
        col("c.last_name"),
        col("c.customer_segment"),
        col("c.city").alias("customer_city"),
        col("c.country"),

        col("s.store_id"),
        col("s.store_name"),
        col("s.city").alias("store_city"),
        col("s.region"),
        col("s.channel").alias("store_channel"),

        col("p.product_id"),
        col("p.sku"),
        col("p.product_name"),
        col("p.category"),
        col("p.brand"),

        col("oi.quantity"),

        # Métricas monetarias tipadas
        col("oi.unit_price")
            .cast(DecimalType(18, 2))
            .alias("unit_price"),

        col("oi.discount_amount")
            .cast(DecimalType(18, 2))
            .alias("discount_amount"),

        col("oi.line_total")
            .cast(DecimalType(18, 2))
            .alias("line_total"),

        col("o.payment_method"),
        col("o.sales_channel")
    )
)


# ============================================================
# Mostrar Gold
# ============================================================

print("")
print("=== GOLD SALES ===")

gold_sales.printSchema()

gold_sales.show(
    truncate=False
)

print(
    f"Registros Gold: {gold_sales.count()}"
)


# ============================================================
# Escribir Gold
# ============================================================

gold_path = f"s3a://{BUCKET}/gold/sales"

(
    gold_sales
    .write
    .mode("overwrite")
    .parquet(gold_path)
)


print("")
print("=== GOLD SALES GENERADA ===")
print(gold_path)


# ============================================================
# Finalización
# ============================================================

spark.stop()