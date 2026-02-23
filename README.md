# Marketing ETL Pipeline  
**Apache Airflow + BigQuery + dbt + Docker**

---

## 📌 Project Overview

This project implements a production-style marketing data pipeline that simulates how modern companies ingest, transform, and analyze advertising data.

The pipeline:

1. Extracts marketing performance data via API (Python)
2. Loads raw data into BigQuery
3. Transforms data using dbt
4. Orchestrates workflows using Airflow
5. Produces analytics-ready tables for dashboards

The goal is to demonstrate real-world data engineering skills in orchestration, warehousing, transformation, and reproducibility.

---

## 🏗 Architecture

```
External Marketing API
        ↓
Python Extraction Script
        ↓
Airflow DAG (Dockerized)
        ↓
BigQuery (Raw Dataset)
        ↓
dbt Transformations
        ↓
Analytics Tables (Mart Layer)
        ↓
BI Dashboard (Looker Studio)
```

### Components

- Orchestration: Apache Airflow
- Warehouse: BigQuery
- Transformation: dbt
- Metadata DB: PostgreSQL
- Containerization: Docker
- Version Control: GitHub

---

## 📂 Repository Structure

```
marketing-etl-airflow-bq-dbt/
│
├── dags/                      # Airflow DAG definitions
│   └── marketing_etl_dag.py
│
├── src/                       # Python extraction logic
│   └── extract_marketing_data.py
│
├── dbt/                       # dbt project
│   ├── models/
│   └── dbt_project.yml
│
├── docs/                      # Architecture & design diagrams
│   └── architecture.png
│
├── Dockerfile
├── docker-compose.yml
├── requirements.in
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup Instructions

### 1️⃣ Clone repository

```
git clone <repo-url>
cd marketing-etl-airflow-bq-dbt
```

### 2️⃣ Start services

```
docker compose up --build
```

### 3️⃣ Access Airflow UI

```
http://localhost:8080
```

---

## 🗃 Data Model

### Raw Layer
- raw_marketing_campaigns
- raw_ads
- raw_ad_sets

### Staging Layer (dbt)
- stg_campaigns
- stg_ads

### Mart Layer
- fct_marketing_performance
- dim_campaign
- dim_date

---

## 📊 Metrics Implemented

- Click Through Rate (CTR)
- Cost Per Click (CPC)
- Cost Per Acquisition (CPA)
- Return on Ad Spend (ROAS)
- Daily Spend
- Conversion Rate

---

## 🧪 Data Quality & Testing

- dbt tests (not null, unique, relationships)
- Incremental model validation
- Structured logging in Python
- Idempotent loads
- Retry logic in Airflow tasks

---

## 🔁 Orchestration Design

The Airflow DAG is structured into modular tasks:

- extract_task
- load_raw_task
- transform_dbt_task
- data_quality_task

Key features:

- Retry configuration
- Failure handling
- Clear task dependencies
- Parameterized execution

---

## 🔐 Reproducibility

- Fully Dockerized environment
- Version-pinned dependencies
- Airflow constraints respected
- Environment variables managed via `.env`

---

## 💰 Cost Optimization

BigQuery usage is optimized by:

- Partitioned tables
- Incremental loads
- Limited raw ingestion size
- Separation of raw and mart datasets

---

## 🚀 Future Improvements

- CI/CD via GitHub Actions
- Slack failure alerts
- Data quality monitoring dashboard
- Infrastructure as Code (Terraform)
- Secrets management with GCP Secret Manager

---

## 🎯 What This Project Demonstrates

- Workflow orchestration
- Data warehouse modeling
- Production-aware design
- Dependency management
- Cloud data engineering fundamentals
- Clean repository structure

---

## 👤 Author

Aspiring Data Engineer building production-style pipelines with modern data stack tools.
