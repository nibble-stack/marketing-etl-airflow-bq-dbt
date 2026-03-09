# Marketing ETL Pipeline  

<p align="center">
  <strong>Apache Airflow • BigQuery • dbt • Docker • Python</strong>
</p>

---

## 🧰 Tech Stack

![Airflow](https://img.shields.io/badge/Airflow-017CEE?logo=apache-airflow&logoColor=white)
![BigQuery](https://img.shields.io/badge/BigQuery-669DF6?logo=google-bigquery&logoColor=white)
![dbt](https://img.shields.io/badge/dbt-FF694B?logo=dbt&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)

---

## 📌 Project Overview

This project implements a **production-style marketing data pipeline** using modern data engineering tools.  
It simulates how real companies ingest, transform, and model advertising performance data.

The pipeline:

1. Extracts weather data and generates synthetic marketing metrics  
2. Loads data into a **BigQuery staging table**  
3. MERGEs staging → raw (idempotent ingestion)  
4. Transforms data using **dbt (staging + marts)**  
5. Produces analytics-ready fact tables for BI dashboards  

This project demonstrates a complete, cloud‑native data engineering workflow.

---

<details open>
  <summary><strong>📚 Table of Contents</strong></summary>

- [🏗 Architecture](#-architecture)
- [📂 Repository Structure](#-repository-structure)
- [⚙️ Setup Instructions](#️-setup-instructions)
- [🗃 Data Model](#-data-model)
- [📊 Metrics Implemented](#-metrics-implemented)
- [🧪 Data Quality & Testing](#-data-quality--testing)
- [🔁 Orchestration Design](#-orchestration-design)
- [🔐 Reproducibility & Security](#-reproducibility--security)
- [🚀 Future Improvements](#-future-improvements)
- [🎯 What This Project Demonstrates](#-what-this-project-demonstrates)
- [👤 Author](#-author)

</details>

---

## 🏗 Architecture

```
External API (Weather → Synthetic Marketing)
        ↓
Python Extraction (Deterministic Synthetic Metrics)
        ↓
Airflow DAG (Dockerized)
        ↓
BigQuery Staging (stg_marketing_YYYYMMDD_HHMMSS)
        ↓
BigQuery Raw (MERGE, partitioned, clustered)
        ↓
dbt Staging (stg_marketing)
        ↓
dbt Mart (fct_marketing_performance)
        ↓
BI Dashboard (Looker Studio)
```

---

## 📂 Repository Structure

```
marketing-etl-airflow-bq-dbt/
│
├── dags/
│   └── marketing_etl_dag.py
│
├── src/
│   └── extract_marketing_data.py
│
├── dbt/
│   ├── models/
│   │   ├── staging/
│   │   │   ├── stg_marketing.sql
│   │   │   └── stg_marketing.yml
│   │   ├── marts/
│   │   │   ├── fct_marketing_performance.sql
│   │   │   └── fct_marketing_performance.yml
│   │   └── schema.yml
│   └── dbt_project.yml
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup Instructions

### 1️⃣ Clone repository
```
git clone https://github.com/nibble-stack/marketing-etl-airflow-bq-dbt.git
cd marketing-etl-airflow-bq-dbt
```

### 2️⃣ Google Cloud Setup (Required)

To run this project, **you must create your own Google Cloud Platform (GCP) project** to ensure secure and cost-effective usage of BigQuery. Here's how to set it up:

1. **Create a Google Cloud project**  
   Navigate to the [GCP Console](https://console.cloud.google.com/), and create a new project.  
2. **Enable BigQuery API**  
   Go to the APIs & Services section and enable the **BigQuery API** for your project.
3. **Create a Service Account**  
   Create a new service account in your GCP project with the **BigQuery Admin** role.
4. **Generate Service Account Key**  
   Download the service account key as a JSON file.
5. **Place the Key in the Project**  
   Create a `keys/` directory in this repository relative to the root and move your JSON key in the keys folder

6. **Update the `.env` File**  
   Create your own `.env` based on this repo's `.env.example` file and provide the following configuration, replacing the placeholders with your own values:

```env
GCP_PROJECT_ID=your-project-id
BIGQUERY_DATASET=your-dataset-name
GOOGLE_APPLICATION_CREDENTIALS=/opt/airflow/keys/bq-service-account.json
```

### 3️⃣ Start services
```
export AIRFLOW_UID=$(id -u)
docker compose up --build
```

### 4️⃣ Access Airflow
```
http://localhost:8080
username: admin
password: admin123
```

---

## 🗃 Data Model

### **Raw Layer (BigQuery)**
- `raw_marketing_data`  
  - Partitioned by `DATE(timestamp)`  
  - Clustered by `timestamp`  
  - Loaded via MERGE (idempotent)

### **Staging Layer (dbt)**
- `stg_marketing`  
  - Thin, cleaned version of raw data  
  - Adds `date` column  
  - Enforces naming consistency  

### **Mart Layer (dbt)**
- `fct_marketing_performance`  
  - Daily aggregated marketing KPIs  
  - Analytics-ready fact table  

---

## 📊 Metrics Implemented

Even though the data comes from a weather API, dbt transforms it into marketing-style KPIs:

- **CTR**  
- **CPC**  
- **CPA**  
- **ROAS**  
- **Conversion Rate**  
- **Daily Spend**  
- **Daily Impressions**  
- **Daily Clicks**  
- **Daily Conversions**  

---

## 🧪 Data Quality & Testing

- dbt tests:
- `unique` + `not_null` on primary keys  
- Column-level documentation  
- BigQuery schema enforcement  
- Idempotent MERGE ingestion  
- Airflow retries + logging  

---

## 🔁 Orchestration Design

Airflow DAG tasks:

- `extract_marketing_data`  
- `load_raw_bigquery`  
- `run_dbt_models`  

Features:

- Clear task dependencies  
- Idempotent ingestion  
- Modular Python functions  
- Dockerized Airflow environment  

---

## 🔐 Reproducibility & Security

- Fully Dockerized  
- Version-pinned dependencies  
- `.env.example` for environment variables  
- No credentials committed  
- GCP service account isolated to your project  

---

## 🚀 Future Improvements

- CI/CD with GitHub Actions  
- Slack alerts for pipeline failures  
- Data quality dashboard  
- Terraform for infrastructure provisioning  
- Additional fact/dimension models  

---

## 🎯 What This Project Demonstrates

- Cloud-native data engineering  
- BigQuery warehouse modeling  
- dbt transformations & testing  
- Airflow orchestration  
- Production-grade ingestion patterns  
- Secure and reproducible pipelines  

---

## 👤 Author

Aspiring Data Engineer focused on building scalable, maintainable, and cloud-native data pipelines using modern tools and best practices.
