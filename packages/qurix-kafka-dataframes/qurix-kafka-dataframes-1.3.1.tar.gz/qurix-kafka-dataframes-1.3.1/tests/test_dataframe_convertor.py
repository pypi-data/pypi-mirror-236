import pandas as pd
import pytest

from qurix.kafka.dataframes.dataframe_convertor import (
    AvroDataFrameConvertor,
    JsonDataFrameConvertor,
)


class TestJsonDataFrameConvertor:
    @pytest.fixture
    def json_converter(self):
        return JsonDataFrameConvertor()

    def test_convert(self, json_converter):
        data = {"Name": ["John", "Jane", "Mike"], "Age": [25, 30, 35]}
        df = pd.DataFrame(data)

        result = json_converter.convert(df)

        assert isinstance(result, str)
        assert len(result) > 0
        assert "John" in result
        assert "Jane" in result
        assert "Mike" in result

    def test_serialize(self, json_converter):
        json_data = [{"Name": "John", "Age": 25}, {"Name": "Jane", "Age": 30}]
        result = json_converter.serialize(json_data)

        assert isinstance(result, str)
        assert len(result) > 0
        assert "John" in result
        assert "Jane" in result
        assert "Age" in result

    def test_deserialize(self, json_converter):
        json_string = '[{"Name": "John", "Age": 25}, {"Name": "Jane", "Age": 30}]'
        result = json_converter.deserialize(json_string)

        assert isinstance(result, pd.DataFrame)
        assert len(result) == 2
        assert "Name" in result.columns
        assert "Age" in result.columns


class TestAvroDataFrameConvertor:
    @pytest.fixture
    def avro_converter(self):
        return AvroDataFrameConvertor()

    def test_convert(self, avro_converter):
        data = {"Name": ["John", "Jane", "Mike"], "Age": [25, 30, 35]}
        df = pd.DataFrame(data)

        result = avro_converter.convert(df)

        assert isinstance(result, list)
        assert "Name" in result[0]
        assert "Age" in result[0]

    def test_serialize(self, avro_converter):
        avro_schema = {
            "type": "record",
            "name": "DataFrame",
            "fields": [
                {"name": "Name", "type": "string"},
                {"name": "Age", "type": "int"},
            ],
        }
        records = [{"Name": "John", "Age": 25}, {"Name": "Jane", "Age": 30}]
        avro_converter = AvroDataFrameConvertor(avro_schema=avro_schema)

        result = avro_converter.serialize(records)

        assert isinstance(result, bytes)
        assert len(result) > 0

    def test_deserialize(self, avro_converter):
        avro_schema = {
            "type": "record",
            "name": "DataFrame",
            "fields": [
                {"name": "Name", "type": "string"},
                {"name": "Age", "type": "int"},
            ],
        }
        records = [{"Name": "John", "Age": 25}, {"Name": "Jane", "Age": 30}]

        avro_converter = AvroDataFrameConvertor(avro_schema=avro_schema)
        avro_data = avro_converter.serialize(records)

        result = avro_converter.deserialize(avro_data)
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 2
