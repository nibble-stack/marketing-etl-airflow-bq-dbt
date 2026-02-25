"""
Marketing Data Extraction Module

Fetches weather data from the Open‑Meteo API and enriches it with
synthetic marketing metrics (impressions, clicks, spend, conversions).

This simulates a real marketing API while keeping the pipeline realistic.
"""

import logging
import requests
from datetime import datetime, timezone
from typing import List, Dict
import random

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


# -------------------------------------------------------------------
# API Extraction
# -------------------------------------------------------------------

OPEN_METEO_URL = (
    "https://api.open-meteo.com/v1/forecast"
    "?latitude=52.52&longitude=13.41"
    "&hourly=temperature_2m,precipitation"
)


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
        raise Exception("Failed to fetch data from Open‑Meteo")

    logger.info("Weather data successfully retrieved.")
    return response.json()


# -------------------------------------------------------------------
# Transform Weather → Synthetic Marketing Data
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
        # Synthetic marketing metrics
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
# Placeholder BigQuery Loader (to be replaced in next step)
# -------------------------------------------------------------------


def load_to_bigquery(**context):
    """
    Placeholder for BigQuery loading logic.
    Airflow will pass XCom data here.
    """

    logger.info("Loading data to BigQuery...")

    # Example:
    # ti = context["ti"]
    # records = ti.xcom_pull(task_ids="extract_task")

    logger.info("Data successfully loaded to BigQuery (placeholder).")


# -------------------------------------------------------------------
# TEMPORARY DEBUGGING BLOCK - remove before push
# -------------------------------------------------------------------
if __name__ == "__main__":
    import json
    from datetime import datetime, timezone

    records = extract_data()

    # Limit debug output
    MAX_DEBUG_RECORDS = 1
    debug_records = records[:MAX_DEBUG_RECORDS]

    # Create timestamped filename
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    filename = f"sample_output_{timestamp}.json"

    with open(filename, "w") as f:
        json.dump(debug_records, f, indent=4)

    print(f"Wrote {len(debug_records)} records to {filename}")
