# Architecture Diagram

```mermaid
flowchart TD

    A[Marketing API] --> B[Python Extraction]
    B --> C[Airflow DAG]
    C --> D[BigQuery Raw Dataset]
    D --> E[dbt Transformations]
    E --> F[Analytics Mart]
    F --> G[Looker Studio Dashboard]

    C --> H[PostgreSQL Metadata DB]
