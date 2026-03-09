# tests/test_bigquery_loaders.py

from unittest.mock import patch, MagicMock
from src.extract_marketing_data import load_to_bigquery_temp, load_temp_to_raw


@patch("google.cloud.bigquery.Client")
def test_load_to_bigquery_temp(mock_client):
    mock_instance = mock_client.return_value
    mock_job = MagicMock()
    mock_instance.load_table_from_json.return_value = mock_job

    records = [{"timestamp": "2024-01-01T00:00"}]

    table_name = load_to_bigquery_temp(records)

    assert "stg_marketing_" in table_name
    mock_instance.load_table_from_json.assert_called_once()


@patch("google.cloud.bigquery.Client")
def test_load_temp_to_raw(mock_client):
    mock_instance = mock_client.return_value
    mock_instance.get_table.side_effect = Exception("not found")

    load_temp_to_raw("project.dataset.stg_marketing_123")

    # Table creation should be attempted
    mock_instance.create_table.assert_called_once()

    # MERGE query should be executed
    mock_instance.query.assert_called_once()
