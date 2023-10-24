import pandas as pd
import pytest

from qurix.kafka.dataframes.dataframe_consumer import DataFrameConsumer
from qurix.kafka.dataframes.dataframe_convertor import JsonDataFrameConvertor
from tests.common import KAFKA_TEST_CONFIG


@pytest.fixture
def kafka_conf() -> dict:
    return KAFKA_TEST_CONFIG


class MockMessage:
    def __init__(self, headers: dict, offset: int, partition: str, value=None):
        self._headers = headers
        self._partition = partition
        self._offset = offset
        self._value = value

    def headers(self):
        return self._headers

    def partition(self):
        return self._partition

    def offset(self):
        return self._offset

    def value(self):
        return self._value


sample_dataframe_data = {"name": ["Alice", "Bob"], "age": [30, 25]}
sample_dataframe = pd.DataFrame(sample_dataframe_data)


# Test cases
def test_build_header_df(kafka_conf: dict):
    consumer = DataFrameConsumer(kafka_conf)
    mock_message = MockMessage(
        headers={"header_key": "header_value"}, partition=0, offset=0)
    result_df = consumer.build_header_df(mock_message)

    assert isinstance(result_df, pd.DataFrame)
    assert "header_key" in result_df.columns
    assert "Partition" in result_df.columns
    assert "Offset" in result_df.columns
    assert result_df.at[0, "header_key"] == "header_value"
    assert result_df.at[0, "Partition"] == 0
    assert result_df.at[0, "Offset"] == 0


def test_get_dataframe_id(kafka_conf: dict):
    consumer = DataFrameConsumer(kafka_conf)
    headers = [("data_container_id", b"my_dataframe")]
    result = consumer.get_dataframe_id(headers)
    assert result == "my_dataframe"


def test_get_converter_strategy_json(kafka_conf: dict):
    consumer = DataFrameConsumer(kafka_conf)
    headers = [("format_type", b"json")]
    converter = consumer.get_converter_strategy(headers)
    assert isinstance(converter, JsonDataFrameConvertor)


def test_get_converter_strategy_invalid_format(kafka_conf: dict):
    consumer = DataFrameConsumer(kafka_conf)
    headers = [("format_type", b"invalid_format")]
    with pytest.raises(ValueError):
        consumer.get_converter_strategy(headers)


def test_consume_dataframes(kafka_conf: dict):
    consumer = DataFrameConsumer(kafka_conf)
    result = consumer.consume_dataframes("my_topic", group="test_group")
    assert isinstance(result, list)
    assert len(result) == 0
