from pyspark.sql import SparkSession
from pyspark.sql.functions import col, trim


# ============================================================
# Spark Session
# ============================================================

spark = (
    SparkSession.builder
    .appName("BronzeToSilver")
    # MinIO / S3A
    .config(
        "spark.hadoop.fs.s3a.endpoint",
        "http://minio:9000"
    )
    .config(
        "spark.hadoop.fs.s3a.access.key",
        "admin"
    )
    .config(
        "spark.hadoop.fs.s3a.secret.key",
        "admin123"
    )
    .config(
        "spark.hadoop.fs.s3a.path.style.access",
        "true"
    )
    .config(
        "spark.hadoop.fs.s3a.impl",
        "org.apache.hadoop.fs.s3a.S3AFileSystem"
    )
    .config(
        "spark.hadoop.fs.s3a.connection.ssl.enabled",
        "false"
    )

    .getOrCreate()
)


# ============================================================
# Configuración
# ============================================================

BUCKET = "enterprise-sales"

TABLES = [
    "customers",
    "products",
    "stores",
    "orders",
    "order_items",
]


# ============================================================
# Procesamiento Bronze -> Silver
# ============================================================

for table in TABLES:

    print("")
    print("=" * 60)
    print(f"PROCESANDO: {table}")
    print("=" * 60)

    bronze_path = (
        f"s3a://{BUCKET}/"
        f"bronze/{table}/{table}.json"
    )

    silver_path = (
        f"s3a://{BUCKET}/"
        f"silver/{table}"
    )

    print(f"Bronze: {bronze_path}")
    print(f"Silver: {silver_path}")

    # --------------------------------------------------------
    # Leer Bronze
    # --------------------------------------------------------

    df = (
        spark.read
        .option("multiLine", True)
        .json(bronze_path)
    )

    print("Esquema Bronze:")
    df.printSchema()

    bronze_count = df.count()

    print(f"Registros Bronze: {bronze_count}")

    # --------------------------------------------------------
    # Limpieza básica
    # --------------------------------------------------------

    # Eliminar espacios en columnas string
    for field in df.schema.fields:

        if field.dataType.simpleString() == "string":
            df = df.withColumn(
                field.name,
                trim(col(field.name))
            )

    # --------------------------------------------------------
    # Validación básica
    # --------------------------------------------------------

    silver_count = df.count()

    print(f"Registros después de transformación: {silver_count}")

    if bronze_count != silver_count:
        raise ValueError(
            f"ERROR: cantidad de registros cambió en {table}. "
            f"Bronze={bronze_count}, Silver={silver_count}"
        )

    # --------------------------------------------------------
    # Escribir Silver
    # --------------------------------------------------------

    (
        df.write
        .mode("overwrite")
        .parquet(silver_path)
    )

    print(f"✓ Silver generada correctamente: {table}")
    print(f"✓ Registros Silver: {silver_count}")


# ============================================================
# Finalización
# ============================================================

print("")
print("=" * 60)
print("BRONZE -> SILVER COMPLETADO")
print("=" * 60)

spark.stop()