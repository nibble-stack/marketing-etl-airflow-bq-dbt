import pytest
from src.extract_marketing_data import transform_record


def test_transform_record_structure():
    sample_input = {"campaign_id": "123", "clicks": 100, "spend": 50.0}

    result = transform_record(sample_input)

    assert "campaign_id" in result
    assert "clicks" in result
    assert "spend" in result


def test_transform_record_types():
    sample_input = {"campaign_id": "123", "clicks": "100", "spend": "50.0"}

    result = transform_record(sample_input)

    assert isinstance(result["clicks"], int)
    assert isinstance(result["spend"], float)
