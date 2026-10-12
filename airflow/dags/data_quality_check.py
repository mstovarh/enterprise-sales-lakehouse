import json

from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.amazon.aws.hooks.s3 import S3Hook

from datetime import datetime


TABLES = [
    "customers",
    "products",
    "stores",
    "orders",
    "order_items",
]


def validate_table(table_name):

    # PostgreSQL
    postgres = PostgresHook(
        postgres_conn_id="novaretail_postgres"
    )

    connection = postgres.get_conn()
    cursor = connection.cursor()

    cursor.execute(
        f"SELECT COUNT(*) FROM erp.{table_name}"
    )

    source_count = cursor.fetchone()[0]

    cursor.close()
    connection.close()

    # MinIO
    minio = S3Hook(
        aws_conn_id="novaretail_minio"
    )

    key = f"bronze/{table_name}/{table_name}.json"

    data = minio.read_key(
        key=key,
        bucket_name="enterprise-sales"
    )

    records = json.loads(data)

    bronze_count = len(records)

    print(f"Tabla: {table_name}")
    print(f"PostgreSQL: {source_count}")
    print(f"Bronze: {bronze_count}")

    if source_count != bronze_count:
        raise ValueError(
            f"DATA QUALITY FAILED: {table_name}"
        )

    print(
        f"DATA QUALITY PASSED: {table_name} ✅"
    )


with DAG(
    dag_id="data_quality_check",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
    tags=["data-quality"],
) as dag:

    for table in TABLES:

        PythonOperator(
            task_id=f"validate_{table}",
            python_callable=validate_table,
            op_kwargs={
                "table_name": table
            },
        )