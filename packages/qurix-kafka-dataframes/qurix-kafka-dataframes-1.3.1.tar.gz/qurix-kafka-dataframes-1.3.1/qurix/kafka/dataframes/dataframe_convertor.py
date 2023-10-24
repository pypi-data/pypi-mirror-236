import io
import json
from typing import Any

import fastavro
import pandas as pd

from qurix.kafka.dataframes.base_dataframe_convertor import \
    BaseDataFrameConvertor


class JsonDataFrameConvertor(BaseDataFrameConvertor):
    @staticmethod
    def convert(df: pd.DataFrame) -> json:
        json_data = df.to_json(orient="records")
        return json_data

    @staticmethod
    def serialize(json_data: json) -> json:
        data = json.dumps(json_data)
        return data

    @staticmethod
    def deserialize(input: json) -> pd.DataFrame:
        data = json.loads(input)

        if isinstance(data, list):
            dataframe = pd.DataFrame(data)
        else:
            dataframe = pd.DataFrame([data])

        return dataframe


class AvroDataFrameConvertor(BaseDataFrameConvertor):
    def __init__(self, avro_schema: dict = None):
        self.avro_schema = avro_schema

    def generate_avro_schema(self, df: pd.DataFrame) -> dict:
        # Generate Avro schema based on DataFrame's columns and data types
        fields = []
        for column, dtype in df.dtypes.items():
            field_type = self.map_pandas_dtype_to_avro(dtype)
            fields.append({"name": column, "type": field_type})
        avro_schema = {"type": "record", "name": "DataFrame", "fields": fields}
        return avro_schema

    def map_pandas_dtype_to_avro(self, dtype: str | Any) -> str:
        # Map Pandas data types to corresponding Avro types
        dtype_mapping = {
            "int64": "int",
            "float64": "double",
            "object": "string",
        }
        return dtype_mapping.get(str(dtype), "string")

    def convert(self, df: pd.DataFrame) -> dict:
        if not self.avro_schema:
            self.avro_schema = self.generate_avro_schema(df)

        print("Avro schema:", self.avro_schema)
        records = df.to_dict(orient="records")
        return records

    def serialize(self, records: dict) -> bytearray:
        if not self.avro_schema:
            raise ValueError("Avro schema is missing.")
        with io.BytesIO() as avro_data:
            fastavro.writer(avro_data, self.avro_schema, records)
            return avro_data.getvalue()

    def deserialize(self, input: bytearray) -> pd.DataFrame:
        # Create a buffer from the input data
        buffer = io.BytesIO(input)

        # Deserialize the Avro data using the Avro schema and the buffer
        reader = fastavro.reader(buffer, reader_schema=self.avro_schema)

        # Convert the Avro records to a list of dictionaries
        records = list(reader)

        # Convert the list of dictionaries to a DataFrame
        df = pd.DataFrame.from_records(records)

        return df
