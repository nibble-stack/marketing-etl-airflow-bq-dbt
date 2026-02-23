"""
Marketing Data Extraction Module

Responsible for:
- Fetching marketing data (simulated or real API)
- Basic validation
- Preparing data for warehouse load
"""

import logging
import random
from datetime import datetime
from typing import List, Dict

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


# -------------------------------------------------------------------
# Simulated API Extraction
# -------------------------------------------------------------------


def extract_data(**context) -> List[Dict]:
    """
    Simulates extracting marketing data from an API.

    Returns:
        List of campaign performance records.
    """

    logger.info("Starting marketing data extraction...")

    # Simulated marketing metrics
    data = []

    for campaign_id in range(1, 6):
        record = {
            "campaign_id": campaign_id,
            "date": datetime.utcnow().date().isoformat(),
            "clicks": random.randint(50, 500),
            "impressions": random.randint(1000, 10000),
            "spend": round(random.uniform(20.0, 200.0), 2),
        }

        data.append(record)

    logger.info(f"Extracted {len(data)} campaign records.")

    return data


# -------------------------------------------------------------------
# Data Loading (Mock BigQuery Load)
# -------------------------------------------------------------------


def load_to_bigquery(**context):
    """
    Simulates loading data into BigQuery.

    In a real implementation:
    - Initialize BigQuery client
    - Write to partitioned table
    - Handle idempotency
    """

    logger.info("Loading data to BigQuery...")

    # In real pipeline, you would retrieve XCom data:
    # records = context["ti"].xcom_pull(task_ids="extract_marketing_data")

    logger.info("Data successfully loaded to BigQuery (simulated).")
