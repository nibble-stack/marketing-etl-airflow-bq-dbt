# tests/test_generate_marketing_records.py

import pytest
from src.extract_marketing_data import generate_marketing_records

MOCK_API_RESPONSE = {
    "hourly": {
        "time": ["2024-01-01T00:00", "2024-01-01T01:00"],
        "temperature_2m": [20.5, 21.0],
        "precipitation": [0.0, 0.1],
    }
}


def test_generate_marketing_records_length():
    records = generate_marketing_records(MOCK_API_RESPONSE)
    assert len(records) == 2


def test_generate_marketing_records_keys():
    record = generate_marketing_records(MOCK_API_RESPONSE)[0]

    expected_keys = {
        "timestamp",
        "temperature",
        "precipitation",
        "impressions",
        "clicks",
        "conversions",
        "spend",
        "extracted_at",
    }

    assert expected_keys == set(record.keys())


def test_generate_marketing_records_deterministic():
    """Random seed is based on timestamp, so output should be deterministic."""
    r1 = generate_marketing_records(MOCK_API_RESPONSE)
    r2 = generate_marketing_records(MOCK_API_RESPONSE)

    for rec in r1:
        rec.pop("extracted_at", None)
    for rec in r2:
        rec.pop("extracted_at", None)

    assert r1 == r2


def test_generate_marketing_records_value_ranges():
    record = generate_marketing_records(MOCK_API_RESPONSE)[0]

    assert 5000 <= record["impressions"] <= 50000
    assert 0 <= record["clicks"] <= record["impressions"]
    assert 0 <= record["conversions"] <= record["clicks"]
    assert 20 <= record["spend"] <= 200
