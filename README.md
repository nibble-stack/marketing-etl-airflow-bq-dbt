# Marketing ETL Pipeline  

<p align="center">
  <strong>Apache Airflow + BigQuery + dbt + Docker</strong>
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

This project implements a production-style **marketing data pipeline** that simulates how modern companies ingest, transform, and analyze advertising data.

The pipeline:

1. Extracts marketing-like data via API (Python)  
2. Loads raw data into BigQuery  
3. Transforms data using dbt  
4. Orchestrates workflows using Airflow  
5. Produces analytics-ready tables for dashboards  

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
External API (Weather → Marketing Simulation)
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
│   └── dbt_project.yml
│
├── docs/
│   └── architecture.md
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
cd marketing-etl-airflow-bq_dbt
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

Note: This ensures security and cost isolation.


### 3️⃣ Start services
```
export AIRFLOW_UID=$(id -u)
docker compose up --build
```

### 4️⃣ Access Airflow
```
- URL: http://localhost:8080
- Username: admin
- Password: admin123
```

---

## 🗃 Data Model

### Raw Layer
- raw_weather (simulated marketing data)

### Staging Layer (dbt)
- stg_weather

### Mart Layer
- fct_marketing_performance  
- dim_date  

---

## 📊 Metrics Implemented

Even though the data comes from a weather API, dbt transforms it into marketing-style KPIs:

- CTR  
- CPC  
- CPA  
- ROAS  
- Daily Spend  
- Conversion Rate  

---

## 🧪 Data Quality & Testing

- dbt tests (unique, not null, relationships)  
- Incremental model validation  
- Structured logging in Python  
- Idempotent loads  
- Retry logic in Airflow tasks  

---

## 🔁 Orchestration Design

Airflow DAG tasks:

- `extract_task`  
- `load_raw_task`  
- `transform_dbt_task`  
- `data_quality_task`  

Features:

- Retries  
- Failure handling  
- Clear dependencies  
- Parameterized execution  

---

## 🔐 Reproducibility

- Fully Dockerized  
- Version-pinned dependencies  
- Airflow constraints respected  
- `.env.example` for environment variables  
- No credentials or sensitive files exposed

---

## 🚀 Future Improvements

- CI/CD with GitHub Actions  
- Slack alerts  
- Data quality dashboard  
- Terraform IaC  
- GCP Secret Manager  

---

## 🎯 What This Project Demonstrates

- Workflow orchestration: Apache Airflow
- Data warehouse modeling: dbt and BigQuery
- Production-ready pipeline Design: Docker
- Efficient task dependency management
- Cloud data engineering fundamentals  
- Secure handling of cloud credentials and costs

---

## 👤 Author

Aspiring Data Engineer committed to building scalable, secure, and maintainable data pipelines with modern tools and best practices in cloud and data engineering.
