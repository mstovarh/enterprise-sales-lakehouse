from datetime import datetime

from airflow import DAG
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator


with DAG(
    dag_id="test_spark_connection",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
    tags=["test", "spark"],
) as dag:

    test_spark = SparkSubmitOperator(
        task_id="test_spark",
        application="/opt/airflow/spark/jobs/read_gold.py",
        conn_id="spark_default",
        name="airflow_test_spark",
        verbose=True,
    )