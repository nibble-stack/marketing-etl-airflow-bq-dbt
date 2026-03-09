from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from airflow.providers.standard.operators.bash import BashOperator
from datetime import datetime
import logging

from src.extract_marketing_data import (
    extract_data,
    load_to_bigquery_temp,
    load_temp_to_raw,
)

logger = logging.getLogger(__name__)

default_args = {
    "owner": "data_engineering",
    "retries": 2,
}


def extract_task_callable(**context):
    """
    Extracts data from API and loads directly into a temporary BigQuery table.
    Only metadata (table name + row count) is pushed to XCom.
    """
    logger.info("Starting data extraction...")

    records = extract_data()
    row_count = len(records)
    logger.info(f"Extracted {row_count} records.")

    # Load directly to BigQuery (no XCom payload)
    temp_table = load_to_bigquery_temp(records)
    logger.info(f"Loaded extracted data into temporary table: {temp_table}")

    # XCom contains only metadata
    return {"temp_table": temp_table, "row_count": row_count}


def load_task_callable(**context):
    """
    Loads data from the temporary table into the final raw BigQuery table.
    """
    ti = context["ti"]
    xcom_data = ti.xcom_pull(task_ids="extract_marketing_data")

    temp_table = xcom_data.get("temp_table")
    row_count = xcom_data.get("row_count")

    if not temp_table:
        raise ValueError("Temporary table name missing from XCom.")

    logger.info(
        f"Loading {row_count} records from {temp_table} into raw table..."
    )
    load_temp_to_raw(temp_table)
    logger.info("Raw load completed successfully.")


with DAG(
    dag_id="marketing_etl",
    start_date=datetime(2024, 1, 1),
    schedule="@daily",
    catchup=False,
    default_args=default_args,
    tags=["marketing", "production"],
) as dag:

    extract_task = PythonOperator(
        task_id="extract_marketing_data",
        python_callable=extract_task_callable,
    )

    load_task = PythonOperator(
        task_id="load_raw_bigquery",
        python_callable=load_task_callable,
    )

    dbt_transform = BashOperator(
        task_id="run_dbt_models",
        bash_command="cd /opt/airflow/dbt && dbt run",
    )

    extract_task >> load_task >> dbt_transform
