# NovaRetail — Enterprise Sales Lakehouse

End-to-end Data Engineering project that implements a modern **Lakehouse architecture** for processing and analyzing retail sales data.

The project simulates the data platform of **NovaRetail**, integrating operational data from PostgreSQL, object storage with MinIO, distributed processing with Apache Spark, analytical transformation with dbt and DuckDB, orchestration with Apache Airflow, and business intelligence with Power BI.

The objective is to demonstrate a complete data pipeline from **operational source systems to business analytics**.

---

## Project Overview

NovaRetail — Enterprise Sales Lakehouse is a complete Data Engineering project designed to simulate a modern analytical data platform for a retail organization.

The solution takes transactional data from an operational PostgreSQL database and processes it through multiple stages until generating analytical datasets consumed by Power BI.

The platform follows a simplified **Bronze / Silver / Gold Lakehouse architecture**.

The complete workflow is:

```text
Operational Data
      ↓
PostgreSQL
      ↓
MinIO / Bronze
      ↓
Data Quality Validation
      ↓
Apache Spark / Silver
      ↓
dbt + DuckDB / Gold
      ↓
Power BI
```

Apache Airflow acts as the orchestration layer responsible for coordinating the different stages of the pipeline and enforcing task dependencies.

The project focuses on demonstrating how different technologies can be integrated into a complete Data Engineering platform rather than implementing an isolated tool or transformation.

---

# Architecture

```text
                         ┌──────────────────────┐
                         │     PostgreSQL       │
                         │   Operational ERP    │
                         └──────────┬───────────┘
                                    │
                                    │ Extract
                                    ▼
                         ┌──────────────────────┐
                         │        MinIO         │
                         │    Bronze Layer      │
                         │   S3-compatible      │
                         └──────────┬───────────┘
                                    │
                                    │ Validate
                                    ▼
                         ┌──────────────────────┐
                         │   Data Quality       │
                         │      Checks          │
                         └──────────┬───────────┘
                                    │
                                    │ Transform
                                    ▼
                         ┌──────────────────────┐
                         │    Apache Spark      │
                         │   Bronze → Silver    │
                         └──────────┬───────────┘
                                    │
                                    │ Analytical
                                    │ transformation
                                    ▼
                         ┌──────────────────────┐
                         │        dbt           │
                         │   Silver → Gold      │
                         │      + DuckDB        │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │      Power BI        │
                         │   Sales Analytics    │
                         └──────────────────────┘


                    ┌─────────────────────────────┐
                    │       Apache Airflow        │
                    │       Orchestration         │
                    └─────────────────────────────┘
```

The architecture separates the platform into different responsibilities:

- **PostgreSQL** provides the operational source data.
- **MinIO** provides S3-compatible object storage for the Bronze layer.
- **Data Quality** validates the extracted datasets before downstream processing.
- **Apache Spark** performs Bronze-to-Silver transformations.
- **dbt** manages analytical transformations and data models.
- **DuckDB** provides the analytical SQL execution engine.
- **Power BI** consumes the final analytical datasets.
- **Apache Airflow** orchestrates the complete workflow.

---

# Technology Stack

| Technology | Purpose |
|---|---|
| **PostgreSQL 16** | Operational source database |
| **Apache Airflow 3.x** | Pipeline orchestration |
| **MinIO** | S3-compatible object storage |
| **Apache Spark 3.5.3** | Data processing and transformation |
| **dbt 1.12** | Analytical transformation and data modeling |
| **DuckDB 1.11** | Analytical SQL engine |
| **Python** | ETL and orchestration logic |
| **Docker** | Containerized infrastructure |
| **Power BI** | Business intelligence and visualization |
| **Git / GitHub** | Version control |

---

# Data Flow

The platform processes data through the following stages:

```text
┌─────────────────────┐
│   PostgreSQL ERP    │
│ Operational Source  │
└──────────┬──────────┘
           │
           │ Extraction
           ▼
┌─────────────────────┐
│    MinIO / Bronze   │
│    Raw Data Layer   │
└──────────┬──────────┘
           │
           │ Validation
           ▼
┌─────────────────────┐
│    Data Quality     │
│      Controls       │
└──────────┬──────────┘
           │
           │ Transformation
           ▼
┌─────────────────────┐
│  Apache Spark       │
│  Silver Processing  │
└──────────┬──────────┘
           │
           │ Analytical Modeling
           ▼
┌─────────────────────┐
│      dbt + DuckDB   │
│     Gold Models     │
└──────────┬──────────┘
           │
           │ Business Analytics
           ▼
┌─────────────────────┐
│      Power BI       │
│   Sales Dashboard   │
└─────────────────────┘
```

The pipeline follows an **ETL / ELT hybrid approach**:

1. Extract operational data from PostgreSQL.
2. Store raw data in MinIO.
3. Validate the extracted data.
4. Process datasets using Apache Spark.
5. Build analytical models using dbt.
6. Generate business-ready datasets.
7. Consume the analytical layer through Power BI.

---

# Bronze / Silver / Gold

The platform uses a simplified Lakehouse layering strategy.

## Bronze Layer

The Bronze layer contains the raw data extracted from PostgreSQL.

MinIO is used as the object storage platform.

The structure is organized by business entity:

```text
enterprise-sales/
└── bronze/
    ├── customers/
    │   └── customers.json
    │
    ├── products/
    │   └── products.json
    │
    ├── stores/
    │   └── stores.json
    │
    ├── orders/
    │   └── orders.json
    │
    └── order_items/
        └── order_items.json
```

The Bronze layer acts as the raw landing zone of the data platform.

---

## Silver Layer

Apache Spark processes the Bronze datasets and generates the Silver layer.

The main transformation is:

```text
Bronze → Silver
```

The Spark job responsible for this stage is:

```text
spark/jobs/bronze_to_silver.py
```

This stage prepares the datasets for analytical consumption and downstream modeling.

---

## Gold Layer

The Gold layer contains analytical datasets designed for business consumption.

The analytical transformation layer is implemented using **dbt** with **DuckDB**.

The project currently includes models such as:

```text
stg_orders
fct_sales
sales_by_store
```

The Gold layer provides business-oriented metrics and structures that can be consumed by analytical tools such as Power BI.

---

# Airflow Orchestration

Apache Airflow is responsible for orchestrating the complete data pipeline.

The main DAG is:

```text
enterprise_sales_pipeline
```

The DAG coordinates extraction, data quality, Spark processing and dbt transformations.

The execution flow is:

```text
extract_customers
        ↓
validate_customers
        │
        ├─────────────────────┐
        │                     │
extract_products       validate_products
        │                     │
        ├─────────────────────┤
        │                     │
extract_stores         validate_stores
        │                     │
        ├─────────────────────┤
        │                     │
extract_orders         validate_orders
        │                     │
        ├─────────────────────┤
        │                     │
extract_order_items    validate_order_items
        │                     │
        └──────────┬──────────┘
                   ↓
          Bronze → Silver
          Apache Spark
                   ↓
               dbt build
                   ↓
             Gold Layer
```

Each source extraction has an associated validation task.

The Spark transformation only starts after the required validations have completed successfully.

The dbt build executes after the Spark transformation.

This makes the pipeline dependencies explicit and prevents downstream processing when upstream validation fails.

---

# dbt / Analytical Models

dbt is used as the analytical transformation and modeling layer.

The project separates the transformation logic into reusable SQL models.

## Staging

The staging layer prepares source datasets for analytical transformations.

Example:

```text
stg_orders
```

---

## Fact Model

The main analytical fact model is:

```text
fct_sales
```

The model represents sales at the order-item level.

Important fields include:

```text
order_item_id
order_id
customer_id
product_id
store_id
order_date
order_status
payment_method
sales_channel
quantity
line_total
```

This model provides the foundation for downstream analytical aggregations.

---

## Store-Level Analytical Model

The project generates an aggregated model:

```text
sales_by_store
```

The model provides store-level metrics such as:

```text
store_id
store_name
store_city
region
total_orders
total_units
total_sales
average_line_sales
```

This dataset is used as one of the main analytical sources for Power BI.

---

# Power BI

Power BI provides the business intelligence layer of the platform.

The analytical data generated by dbt is consumed to create a sales performance dashboard for NovaRetail.

The dashboard provides an executive view of retail performance.

## Main KPIs

- Total Sales
- Total Orders
- Units Sold
- Active Stores

## Main Visualizations

- Orders and units by store
- Sales by store
- Sales distribution by store
- Average sales per line

The objective of the dashboard is to transform the analytical data generated by the Data Engineering pipeline into information that can support business analysis and decision-making.

---

# Key Engineering Concepts

This project demonstrates practical implementation of several Data Engineering concepts:

### Data Ingestion

Extraction of operational data from PostgreSQL into an object storage layer.

### Lakehouse Architecture

Implementation of Bronze, Silver and Gold processing layers.

### Object Storage

Use of MinIO as an S3-compatible data lake storage layer.

### Workflow Orchestration

Apache Airflow coordinates dependencies between extraction, validation and transformation tasks.

### Data Quality

Validation gates compare source data against the extracted Bronze datasets before allowing downstream processing.

### Distributed Processing

Apache Spark is used to process and transform the Bronze datasets.

### Analytical Modeling

dbt is used to create reusable analytical models and organize SQL transformations.

### Analytical Engine

DuckDB provides the SQL execution engine for analytical transformations.

### Business Intelligence

Power BI consumes the final analytical dataset and presents business-oriented KPIs and visualizations.

### Containerization

Docker provides a reproducible local environment containing the different components of the platform.

### Version Control

Git and GitHub provide version control and documentation for the complete project.

---

# Future Improvements

The current architecture provides a foundation for additional Data Engineering capabilities.

Potential future improvements include:

- Incremental data ingestion
- Change Data Capture (CDC)
- Partitioned Bronze and Silver datasets
- Incremental dbt models
- Slowly Changing Dimensions
- Apache Iceberg or Delta Lake
- Automated CI/CD with GitHub Actions
- Extended data quality checks
- Data lineage
- Pipeline monitoring and observability
- Cloud deployment
- Streaming ingestion with Apache Kafka
- Advanced Power BI analytics

---

# Author

**Maria Tovar**

Data Engineer / Integration Consultant

Areas of interest:

- Data Engineering
- ETL / ELT
- Data Integration
- Cloud Technologies
- Data Platforms
- Analytics
- Modern Data Architecture

---

## Repository

GitHub:

https://github.com/mstovarh/enterprise-sales-lakehouse
