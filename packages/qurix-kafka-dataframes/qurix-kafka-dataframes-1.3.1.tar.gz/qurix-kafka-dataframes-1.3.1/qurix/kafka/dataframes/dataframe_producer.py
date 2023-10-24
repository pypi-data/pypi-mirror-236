import json
import logging
import uuid
from dataclasses import asdict
from typing import Any

import pandas as pd
from confluent_kafka import Producer

from qurix.kafka.dataframes.base_dataframe_convertor import \
    BaseDataFrameConvertor
from qurix.kafka.dataframes.dataframe_convertor import (AvroDataFrameConvertor,
                                                        JsonDataFrameConvertor)
from qurix.kafka.dataframes.header import HeadersGenerator
from qurix.kafka.dataframes.message_formats import MessageFormat


def configure_logging() -> None:
    logging.basicConfig(level=logging.INFO)


class DataFrameProducer:
    def __init__(self,
                 conf: dict,
                 message_format: MessageFormat,
                 avro_schema: dict = None):
        self.conf = conf
        self.producer = self.create_kafka_producer()
        self.message_format = message_format.value
        self.avro_schema = avro_schema
        self.converter = self.get_converter_strategy()
        configure_logging()

    def create_kafka_producer(self) -> Any:
        try:
            producer = Producer(self.conf)
            return producer
        except Exception as e:
            logging.error("Error creating Kafka producer: %s", str(e))
            raise

    def get_converter_strategy(self) -> BaseDataFrameConvertor:
        if self.message_format == "avro":
            return AvroDataFrameConvertor(self.avro_schema)
        elif self.message_format == "json":
            return JsonDataFrameConvertor()
        else:
            raise ValueError(
                "Invalid message_format. Supported formats: 'avro', 'json'")

    def send_dataframe(self,
                       dataframe: pd.DataFrame,
                       kafka_topic: str,
                       batch_size: int | None = None) -> None:
        transaction_id = str(uuid.uuid4())
        try:
            data = self.converter.convert(dataframe)

            if batch_size:
                batches = self.split_into_batches(data, batch_size)
            else:
                batches = [data]

            dataframe_id = str(uuid.uuid4())
            total_batches = len(batches)

            for _batch_num, batch in enumerate(batches, start=1):
                headers = asdict(
                    HeadersGenerator(
                        data_container_id=dataframe_id,
                        dataflow_name="Dataframe",
                        batch_number=str(_batch_num),
                        batch_size=str(total_batches),
                        format_type=self.message_format,
                        records="Snapshot",
                        source="DataframeProducer",
                        target="Confluent_Kafka",
                        transaction_id=transaction_id,
                        dataflow_id="00001",
                    )
                )
                self.producer.produce(
                    kafka_topic, value=batch, headers=headers)
                self.producer.flush()

            logging.info("DataFrame sent successfully to Kafka.")
        except Exception as e:
            logging.error("Error sending DataFrame to Kafka: %s", str(e))

    def split_into_batches(self, data: Any, batch_size: int):
        try:
            if self.message_format == "json":
                json_data = json.loads(data)
                num_rows = len(json_data)
                batches = []
                start_index = 0
                while start_index < num_rows:
                    end_index = min(start_index + batch_size, num_rows)
                    batch = json_data[start_index:end_index]
                    batch_json = self.converter.serialize(batch)
                    batches.append(batch_json)
                    start_index = end_index
                return batches
            elif self.message_format == "avro":
                num_records = len(data)
                batches = []
                start_index = 0
                while start_index < num_records:
                    end_index = min(start_index + batch_size, num_records)
                    batch_data = data[start_index:end_index]
                    batch_avro = self.converter.serialize(batch_data)
                    batches.append(batch_avro)
                    start_index = end_index
                return batches
            else:
                raise ValueError("Invalid message_format")
        except Exception as e:
            logging.error("Error splitting data into batches: %s", str(e))
            raise
