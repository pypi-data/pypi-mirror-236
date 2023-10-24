from types import NoneType
from unittest import mock
from unittest.mock import patch

import pandas as pd
import pytest

from qurix.kafka.dataframes.dataframe_producer import DataFrameProducer
from qurix.kafka.dataframes.message_formats import MessageFormat
from tests.common import KAFKA_TEST_CONFIG


@pytest.fixture
def kafka_config() -> dict:
    return KAFKA_TEST_CONFIG


@pytest.fixture
def sample_dataframe() -> pd.DataFrame:
    data = {"Name": ["John", "Alice", "Bob"], "Age": [25, 30, 35]}
    return pd.DataFrame(data)


@pytest.fixture
def kafka_topic() -> str:
    return "your_kafka_topic"


@pytest.mark.skip("It takes too long. To check")
@patch("confluent_kafka.Producer")
def test_send_dataframe(
    mock_producer,
    kafka_config: dict,
    sample_dataframe: pd.DataFrame,
    kafka_topic: str
):
    producer_instance = mock.Mock()
    mock_producer.return_value = producer_instance
    avro_schema = {
        "type": "record",
        "name": "DataFrame",
        "fields": [
            {"name": "Name", "type": "string"},
            {"name": "Age", "type": "int"},
        ],
    }
    producer = DataFrameProducer(
        kafka_config,
        message_format=MessageFormat.AVRO,
        avro_schema=avro_schema,
    )
    result = producer.send_dataframe(
        sample_dataframe, kafka_topic, batch_size=2)
    assert result is None
    assert isinstance(result, NoneType)
    assert producer_instance.call_count == 0
