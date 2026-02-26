import pytest
from unittest.mock import patch, Mock
from src.extract_marketing_data import extract_data

MOCK_API_RESPONSE = {
    "hourly": {
        "time": ["2024-01-01T00:00"],
        "temperature_2m": [20.5],
        "precipitation": [0.0],
    }
}


@patch("src.extract_marketing_data.requests.get")
def test_extract_data_structure(mock_get):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = MOCK_API_RESPONSE
    mock_get.return_value = mock_response

    records = extract_data()

    assert isinstance(records, list)
    assert len(records) == 1

    record = records[0]

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


@patch("src.extract_marketing_data.requests.get")
def test_extract_data_types(mock_get):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = MOCK_API_RESPONSE
    mock_get.return_value = mock_response

    record = extract_data()[0]

    assert isinstance(record["timestamp"], str)
    assert isinstance(record["temperature"], float)
    assert isinstance(record["precipitation"], float)
    assert isinstance(record["impressions"], int)
    assert isinstance(record["clicks"], int)
    assert isinstance(record["conversions"], int)
    assert isinstance(record["spend"], float)
    assert isinstance(record["extracted_at"], str)


@patch("src.extract_marketing_data.requests.get")
def test_api_failure_raises_exception(mock_get):
    mock_response = Mock()
    mock_response.status_code = 500
    mock_get.return_value = mock_response

    with pytest.raises(Exception):
        extract_data()
