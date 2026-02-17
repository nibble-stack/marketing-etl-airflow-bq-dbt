# Marketing ETL Pipeline (Airflow + BigQuery + dbt)

## Overview

This project simulates a real-world **marketing data pipeline**:

- Extract marketing data (e.g. ads performance) with **Python**
- Orchestrate daily runs with **Airflow**
- Load raw data into **BigQuery**
- Transform it into analytics-ready tables with **dbt**
- Make it easy to build dashboards (e.g. Looker Studio)

The goal is to demonstrate **data engineering skills** in a business-relevant context:
campaign performance, spend, clicks, conversions, and ROI.

## Tech stack

- Python
- Airflow (Docker)
- BigQuery
- dbt
- GitHub

## Repository structure (planned)

```text
marketing-etl-airflow-bq-dbt/
├─ dags/
│  └─ marketing_etl_dag.py
├─ src/
│  └─ extract_marketing_data.py
├─ dbt/
│  ├─ models/
│  └─ dbt_project.yml
├─ docs/
│  └─ architecture-diagram.png (planned)
└─ README.md
