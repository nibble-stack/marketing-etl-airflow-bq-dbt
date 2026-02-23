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
        python_callable=extract_data,
    )

    load_task = PythonOperator(
        task_id="load_raw_bigquery",
        python_callable=load_to_bigquery,
    )

    dbt_transform = BashOperator(
        task_id="run_dbt_models",
        bash_command="cd /opt/airflow/dbt && dbt run",
    )

    extract_task >> load_task >> dbt_transform
