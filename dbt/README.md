# dbt Project

This folder contains the dbt project responsible for transforming raw marketing data into analytics‑ready models.

---

## 📁 Project Structure

```
dbt/
├── models/
│   ├── staging/
│   │   ├── stg_marketing.sql
│   │   └── stg_marketing.yml
│   ├── marts/
│   │   ├── fct_marketing_performance.sql
│   │   └── fct_marketing_performance.yml
│   └── schema.yml
└── dbt_project.yml
```

---

## 🧱 Models

### **Staging Layer**
- `stg_marketing`
- Cleans and standardizes raw data  
- Adds `date` column  
- Enforces naming consistency  
- Thin, transformation-light model  

### **Mart Layer**
- `fct_marketing_performance`
- Daily aggregated marketing KPIs  
- Analytics-ready fact table  
- Computes CTR, CPC, CPA, ROAS, conversion rate, etc.  

---

## 🧪 Tests & Documentation

- Column-level tests (`unique`, `not_null`)  
- YAML-based documentation for all models  
- dbt docs compatible  
- Clear lineage graph:
```
raw_marketing_data → stg_marketing → fct_marketing_performance
```

---

## 🚀 Running dbt

Inside the Airflow container:

```
cd /opt/airflow/dbt
dbt run
dbt test
```

---

## 🎯 Purpose

This dbt project demonstrates:

- Modern analytics engineering practices  
- Clean staging → mart modeling  
- Data quality enforcement  
- Cloud-native warehouse transformations  
