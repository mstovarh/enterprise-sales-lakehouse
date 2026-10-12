from datetime import datetime
import json

from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from airflow.providers.standard.operators.bash import BashOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator

# ============================================================
# CONFIGURACIÓN
# ============================================================

POSTGRES_CONN_ID = "novaretail_postgres"
MINIO_CONN_ID = "novaretail_minio"
SPARK_CONN_ID = "spark_default"

TABLES = [
    "customers",
    "products",
    "stores",
    "orders",
    "order_items",
]


# ============================================================
# EXTRACT
# PostgreSQL → Bronze / MinIO
# ============================================================

def extract_table(table_name: str):

    print(f"=== Iniciando extracción: {table_name} ===")

    # Conexión a PostgreSQL
    postgres = PostgresHook(
        postgres_conn_id=POSTGRES_CONN_ID
    )

    connection = postgres.get_conn()
    cursor = connection.cursor()

    # Obtener datos
    cursor.execute(
        f"SELECT * FROM erp.{table_name}"
    )

    rows = cursor.fetchall()

    # Obtener nombres de columnas
    columns = [
        description[0]
        for description in cursor.description
    ]

    cursor.close()
    connection.close()

    print(f"Registros extraídos: {len(rows)}")
    print(f"Columnas encontradas: {columns}")

    # Convertir filas a diccionarios
    records = []

    for row in rows:

        record = dict(zip(columns, row))
        records.append(record)

    # Convertir a JSON
    data = json.dumps(
        records,
        ensure_ascii=False,
        indent=2,
        default=str
    )

    # Conexión a MinIO
    minio = S3Hook(
        aws_conn_id=MINIO_CONN_ID
    )

    # Ruta Bronze
    key = f"bronze/{table_name}/{table_name}.json"

    # Guardar en MinIO
    minio.load_string(
        string_data=data,
        key=key,
        bucket_name="enterprise-sales",
        replace=True
    )

    print(
        f"=== Extracción completada: {table_name} ==="
    )

    print(
        f"Archivo generado: s3://enterprise-sales/{key}"
    )


# ============================================================
# DATA QUALITY
# PostgreSQL vs Bronze
# ============================================================

def validate_table(table_name: str):

    print(f"=== Iniciando validación: {table_name} ===")

    # --------------------------------------------------------
    # PostgreSQL
    # --------------------------------------------------------

    postgres = PostgresHook(
        postgres_conn_id=POSTGRES_CONN_ID
    )

    connection = postgres.get_conn()
    cursor = connection.cursor()

    cursor.execute(
        f"SELECT COUNT(*) FROM erp.{table_name}"
    )

    source_count = cursor.fetchone()[0]

    cursor.close()
    connection.close()

    # --------------------------------------------------------
    # Bronze / MinIO
    # --------------------------------------------------------

    minio = S3Hook(
        aws_conn_id=MINIO_CONN_ID
    )

    key = f"bronze/{table_name}/{table_name}.json"

    data = minio.read_key(
        key=key,
        bucket_name="enterprise-sales"
    )

    records = json.loads(data)

    bronze_count = len(records)

    # --------------------------------------------------------
    # Resultado
    # --------------------------------------------------------

    print(f"Tabla: {table_name}")
    print(f"PostgreSQL: {source_count}")
    print(f"Bronze: {bronze_count}")

    if source_count != bronze_count:

        raise ValueError(
            f"DATA QUALITY FAILED: {table_name} "
            f"(PostgreSQL={source_count}, Bronze={bronze_count})"
        )

    print(
        f"DATA QUALITY PASSED: {table_name} ✅"
    )


# ============================================================
# DAG MAESTRO
# ============================================================

with DAG(
    dag_id="enterprise_sales_pipeline",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
    tags=[
        "etl",
        "lakehouse",
        "bronze",
        "silver",
        "gold",
        "quality",
        "spark",
        "dbt",
        "duckdb",
        "minio",
    ],
) as dag:

    # ========================================================
    # 1. EXTRACT
    # ========================================================

    extract_customers = PythonOperator(
        task_id="extract_customers",
        python_callable=extract_table,
        op_kwargs={
            "table_name": "customers"
        },
    )

    extract_products = PythonOperator(
        task_id="extract_products",
        python_callable=extract_table,
        op_kwargs={
            "table_name": "products"
        },
    )

    extract_stores = PythonOperator(
        task_id="extract_stores",
        python_callable=extract_table,
        op_kwargs={
            "table_name": "stores"
        },
    )

    extract_orders = PythonOperator(
        task_id="extract_orders",
        python_callable=extract_table,
        op_kwargs={
            "table_name": "orders"
        },
    )

    extract_order_items = PythonOperator(
        task_id="extract_order_items",
        python_callable=extract_table,
        op_kwargs={
            "table_name": "order_items"
        },
    )

    # ========================================================
    # 2. DATA QUALITY
    # ========================================================

    validate_customers = PythonOperator(
        task_id="validate_customers",
        python_callable=validate_table,
        op_kwargs={
            "table_name": "customers"
        },
    )

    validate_products = PythonOperator(
        task_id="validate_products",
        python_callable=validate_table,
        op_kwargs={
            "table_name": "products"
        },
    )

    validate_stores = PythonOperator(
        task_id="validate_stores",
        python_callable=validate_table,
        op_kwargs={
            "table_name": "stores"
        },
    )

    validate_orders = PythonOperator(
        task_id="validate_orders",
        python_callable=validate_table,
        op_kwargs={
            "table_name": "orders"
        },
    )

    validate_order_items = PythonOperator(
        task_id="validate_order_items",
        python_callable=validate_table,
        op_kwargs={
            "table_name": "order_items"
        },
    )

    # ========================================================
    # 3. BRONZE → SILVER
    # ========================================================

    bronze_to_silver = SparkSubmitOperator(
        task_id="bronze_to_silver",
        application="/opt/airflow/spark/jobs/bronze_to_silver.py",
        conn_id=SPARK_CONN_ID,
        name="bronze_to_silver",
        verbose=True,
    )

    dbt_build = BashOperator(
        task_id="dbt_build",
        bash_command=(
            "cd /opt/airflow/dbt/enterprise_sales && "
            "dbt build --profiles-dir ."
        ),
    )

    # ========================================================
    # DEPENDENCIAS
    # ========================================================

    # Cada extracción valida únicamente su propia tabla.

    extract_customers >> extract_products
    extract_products >> extract_stores
    extract_stores >> extract_orders
    extract_orders >> extract_order_items

    extract_customers >> validate_customers
    extract_products >> validate_products
    extract_stores >> validate_stores
    extract_orders >> validate_orders
    extract_order_items >> validate_order_items

    # Bronze → Silver solamente después de TODAS
    # las validaciones.

    [
        validate_customers,
        validate_products,
        validate_stores,
        validate_orders,
        validate_order_items,
    ] >> bronze_to_silver

    # Silver → Gold

    bronze_to_silver >> dbt_build