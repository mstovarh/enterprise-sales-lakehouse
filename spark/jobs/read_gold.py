from pyspark.sql import SparkSession


spark = (
    SparkSession.builder
    .appName("ReadGoldSales")
    .master("local[*]")
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


path = "s3a://enterprise-sales/gold/sales"


df = spark.read.parquet(path)


print("=== GOLD SALES ===")

df.printSchema()

print("=== REGISTROS ===")

df.show(truncate=False)

print(f"Total registros Gold: {df.count()}")


print("=== VALIDACIÓN ===")

df.select(
    "order_id",
    "product_name",
    "customer_segment",
    "store_name",
    "quantity",
    "line_total"
).show(truncate=False)


spark.stop()