"""
Marketing Data Extraction Module

Simulates marketing data by enriching Open-Meteo weather data
with deterministic synthetic performance metrics.

Architecture:
- Extract (API)
- Transform (deterministic synthetic generation)
- Load → Staging (WRITE_TRUNCATE)
- Load → Raw (Idempotent MERGE)
"""

import logging
import requests
from datetime import datetime, timezone
from typing import List, Dict
import random
import os

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

OPEN_METEO_URL = (
    "https://api.open-meteo.com/v1/forecast"
    "?latitude=52.52&longitude=13.41"
    "&hourly=temperature_2m,precipitation"
)


# -------------------------------------------------------------------
# EXTRACT
# -------------------------------------------------------------------


def extract_weather_data() -> Dict:
    """
    Calls the Open‑Meteo API and returns the raw JSON response.

    Returns:
        dict: Raw API response
    """
    logger.info("Requesting weather data from Open‑Meteo API...")

    response = requests.get(OPEN_METEO_URL, timeout=10)

    if response.status_code != 200:
        logger.error(f"API request failed: {response.status_code}")
        raise Exception("Failed to fetch data from Open-Meteo")

    logger.info("Weather data successfully retrieved.")
    return response.json()


# -------------------------------------------------------------------
# TRANSFORM (Deterministic)
# -------------------------------------------------------------------


def generate_marketing_records(api_json: Dict) -> List[Dict]:
    """
    Converts weather data into synthetic marketing performance records.

    Args:
        api_json (dict): Raw API response

    Returns:
        List[Dict]: List of marketing-like records
    """

    logger.info("Transforming weather data into marketing metrics...")

    timestamps = api_json["hourly"]["time"]
    temps = api_json["hourly"]["temperature_2m"]
    rain = api_json["hourly"]["precipitation"]

    records = []

    for ts, temp, rain_val in zip(timestamps, temps, rain):
        # Deterministic seeding ensures idempotent synthetic metrics
        random.seed(ts)

        impressions = random.randint(5_000, 50_000)
        clicks = int(impressions * random.uniform(0.01, 0.08))
        conversions = int(clicks * random.uniform(0.02, 0.15))
        spend = round(random.uniform(20, 200), 2)

        record = {
            "timestamp": ts,
            "temperature": temp,
            "precipitation": rain_val,
            "impressions": impressions,
            "clicks": clicks,
            "conversions": conversions,
            "spend": spend,
            "extracted_at": datetime.now(timezone.utc).isoformat(),
        }

        records.append(record)

    logger.info(f"Generated {len(records)} marketing records.")
    return records


# -------------------------------------------------------------------
# Airflow Task Wrapper
# -------------------------------------------------------------------


def extract_data(**context) -> List[Dict]:
    """
    Airflow-compatible wrapper:
    - Fetches weather data
    - Converts to marketing metrics
    - Returns list of dicts (XCom‑safe)
    """

    logger.info("Starting extraction task...")
    raw_json = extract_weather_data()
    records = generate_marketing_records(raw_json)

    logger.info("Extraction task completed.")
    return records


# -------------------------------------------------------------------
# Load Extracted Data → Temporary BigQuery Table
# -------------------------------------------------------------------


def load_to_bigquery_temp(records: List[Dict]) -> str:
    from google.cloud import bigquery

    logger.info("Loading data to BigQuery...")

    client = bigquery.Client()
    project = os.getenv("GCP_PROJECT_ID")
    dataset = os.getenv("BIGQUERY_DATASET")

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    table_id = f"{project}.{dataset}.stg_marketing_{timestamp}"

    logger.info(
        f"Loading {len(records)} records into staging table {table_id}..."
    )

    job = client.load_table_from_json(
        records,
        table_id,
        job_config=bigquery.LoadJobConfig(
            write_disposition="WRITE_TRUNCATE",
            autodetect=True,
        ),
    )
    job.result()

    logger.info(f"Staging table created: {table_id}")
    return table_id


# -------------------------------------------------------------------
# LOAD → RAW (Idempotent MERGE)
# -------------------------------------------------------------------


def load_temp_to_raw(temp_table: str):
    from google.cloud import bigquery

    client = bigquery.Client()
    project = os.getenv("GCP_PROJECT_ID")
    dataset = os.getenv("BIGQUERY_DATASET")
    raw_table = f"{project}.{dataset}.raw_marketing_data"

    logger.info(
        f"Loading staging table {temp_table} into raw table {raw_table}..."
    )

    # ---------------------------------------------------------
    # 1. Create raw table with explicit schema + partitioning
    # ---------------------------------------------------------
    schema = [
        bigquery.SchemaField("timestamp", "TIMESTAMP"),
        bigquery.SchemaField("temperature", "FLOAT"),
        bigquery.SchemaField("precipitation", "FLOAT"),
        bigquery.SchemaField("impressions", "INT64"),
        bigquery.SchemaField("clicks", "INT64"),
        bigquery.SchemaField("conversions", "INT64"),
        bigquery.SchemaField("spend", "FLOAT"),
        bigquery.SchemaField("extracted_at", "TIMESTAMP"),
    ]

    table = bigquery.Table(raw_table, schema=schema)

    table.time_partitioning = bigquery.TimePartitioning(
        type_=bigquery.TimePartitioningType.DAY,
        field="timestamp",  # partition by date(timestamp)
    )

    table.clustering_fields = ["timestamp"]

    try:
        client.get_table(raw_table)
        logger.info("Raw table already exists — skipping creation.")
    except Exception:
        logger.info(
            "Raw table does not exist — creating with schema + partitioning..."
        )
        client.create_table(table)
        logger.info("Raw table created.")

    # ---------------------------------------------------------
    # 2. MERGE staging → raw (idempotent load)
    # ---------------------------------------------------------
    merge_query = f"""
    MERGE `{raw_table}` T
    USING `{temp_table}` S
    ON T.timestamp = S.timestamp

    WHEN MATCHED THEN
      UPDATE SET
        temperature = S.temperature,
        precipitation = S.precipitation,
        impressions = S.impressions,
        clicks = S.clicks,
        conversions = S.conversions,
        spend = S.spend,
        extracted_at = S.extracted_at

    WHEN NOT MATCHED THEN
      INSERT (
        timestamp,
        temperature,
        precipitation,
        impressions,
        clicks,
        conversions,
        spend,
        extracted_at
      )
      VALUES (
        S.timestamp,
        S.temperature,
        S.precipitation,
        S.impressions,
        S.clicks,
        S.conversions,
        S.spend,
        S.extracted_at
      );
    """

    client.query(merge_query).result()

    logger.info("Raw MERGE load completed.")


# -------------------------------------------------------------------
# TEMPORARY DEBUGGING BLOCK - remove before push
# -------------------------------------------------------------------
# if __name__ == "__main__":
#     import json
#     from datetime import datetime, timezone
#
#     records = extract_data()
#
#     # Limit debug output
#     MAX_DEBUG_RECORDS = 1
#     debug_records = records[:MAX_DEBUG_RECORDS]
#
#     # Create timestamped filename
#     timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
#     filename = f"sample_output_{timestamp}.json"
#
#     with open(filename, "w") as f:
#         json.dump(debug_records, f, indent=4)
#
#     print(f"Wrote {len(debug_records)} records to {filename}")

# -------------------------------------------------------------------
# V2 TEMPORARY DEBUGGING BLOCK - remove before push
# -------------------------------------------------------------------

# if __name__ == "__main__":
#     import json
#
#     # Deterministic sample instead of live API call
#     sample_api_response = {
#         "hourly": {
#             "time": ["2024-01-01T00:00"],
#             "temperature_2m": [21.5],
#             "precipitation": [0.0],
#         }
#     }
#
#     random.seed(42)  # make synthetic metrics reproducible
#
#     records = generate_marketing_records(sample_api_response)
#
#     timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
#     filename = f"sample_output_{timestamp}.json"
#
#     with open(filename, "w") as f:
#         json.dump(records, f, indent=4)
#
#     print(f"Wrote {len(records)} records to {filename}")
