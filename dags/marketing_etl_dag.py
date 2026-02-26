from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime
import logging

from src.extract_marketing_data import extract_data, load_to_bigquery

logger = logging.getLogger(__name__)

default_args = {
    "owner": "data_engineering",
    "retries": 2,
}


def extract_task_callable(**context):
    """Extract data and push to XCom."""
    logger.info("Starting data extraction...")
    records = extract_data()
    logger.info(f"Extracted {len(records)} records.")
    return records  # Airflow automatically pushes return value to XCom


def load_task_callable(**context):
    """Pull extracted data from XCom and load into BigQuery."""
    logger.info(f"Extracted {len(records)} records.")
    ti = context["ti"]
    records = ti.xcom_pull(task_ids="extract_marketing_data")

    if not records:
        raise ValueError(
            "No records found in XCom. Extraction may have failed."
        )

    logger.info(f"Loading {len(records)} records into BigQuery...")
    load_to_bigquery(records)
    logger.info("Load completed successfully.")


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
