import duckdb

con = duckdb.connect("/tmp/enterprise_sales.duckdb")

print("=== EXPORTANDO MODELO PARA POWER BI ===")

con.execute("INSTALL httpfs")
con.execute("LOAD httpfs")

con.execute("""
    CREATE SECRET minio (
        TYPE S3,
        KEY_ID 'admin',
        SECRET 'admin123',
        ENDPOINT 'minio:9000',
        USE_SSL false,
        URL_STYLE 'path'
    )
""")

con.execute("""
    COPY (
        SELECT *
        FROM main.sales_by_store
    )
    TO '/opt/airflow/dags/sales_by_store.csv'
    WITH (
        HEADER,
        DELIMITER ','
    )
""")

print("✓ CSV generado")
print("/opt/airflow/dags/sales_by_store.csv")

con.close()