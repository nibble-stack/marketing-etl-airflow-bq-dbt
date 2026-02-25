# tests/test_extract.py

from src.extract_marketing_data import extract_data


def test_extract_data_structure():
    records = extract_data()

    # Basic structure checks
    assert isinstance(records, list)
    assert len(records) > 0

    first = records[0]
    assert isinstance(first, dict)

    # Expected keys
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

    assert expected_keys.issubset(first.keys())


def test_extract_data_types():
    records = extract_data()
    first = records[0]

    assert isinstance(first["timestamp"], str)
    assert isinstance(first["temperature"], (int, float))
    assert isinstance(first["precipitation"], (int, float))
    assert isinstance(first["impressions"], int)
    assert isinstance(first["clicks"], int)
    assert isinstance(first["conversions"], int)
    assert isinstance(first["spend"], float)
    assert isinstance(first["extracted_at"], str)
