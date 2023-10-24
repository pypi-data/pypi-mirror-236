import logging
from typing import Any

import pandas as pd
from confluent_kafka import Consumer, KafkaException

from qurix.kafka.dataframes.base_dataframe_convertor import \
    BaseDataFrameConvertor
from qurix.kafka.dataframes.dataframe_convertor import (AvroDataFrameConvertor,
                                                        JsonDataFrameConvertor)

logging.basicConfig(filename="logfile.log", level=logging.INFO)


class DataFrameConsumer:
    def __init__(self, conf: dict) -> None:
        self.conf = conf

    def build_header_df(self, message: Any,
                        dataframe: pd.DataFrame | None = None) -> pd.DataFrame:
        headers = dict(message.headers())
        partition = message.partition()
        offset = message.offset()

        # Create a new record for the current message
        new_row = {key: [value] for key, value in headers.items()}
        new_row["Partition"] = partition
        new_row["Offset"] = offset

        # Create a DataFrame if none was passed
        if dataframe is None:
            dataframe = pd.DataFrame(new_row)
        else:
            # Add the new record to the DataFrame
            dataframe = pd.concat(
                [dataframe, pd.DataFrame(new_row)], ignore_index=True)

        return dataframe

    def get_dataframe_id(self, headers: list) -> str:
        for header in headers:
            if header[0] == "data_container_id":
                return header[1].decode("utf-8")
        return "default"

    def get_converter_strategy(self, headers: list) -> BaseDataFrameConvertor:
        message_format = None
        for header_key, header_value in headers:
            if header_key == "format_type":
                message_format = header_value.decode("utf-8")
                break
        if message_format == "avro":
            return AvroDataFrameConvertor()
        elif message_format == "json":
            return JsonDataFrameConvertor()
        else:
            raise ValueError(
                "Invalid message_format. Supported formats: 'avro', 'json'")

    def create_kafka_consumer(self, group: str) -> None:
        conf = self.conf.copy()
        conf["group.id"] = group
        consumer = Consumer(conf)
        return consumer

    def consume_dataframes(self,
                           kafka_topic: str,
                           group="JsonDataFrameConsumer") -> list:
        consumer = self.create_kafka_consumer(group)
        consumer.subscribe([kafka_topic])

        dataframes = {}  # Dictionary for collecting the data frames
        header_df = None

        try:
            while True:
                msg = consumer.poll(5.0)

                if msg is None:
                    logging.info("No further data in topic")
                    break
                elif msg.error():
                    logging.error("KafkaException occurred: %s", msg.error())
                    raise KafkaException(msg.error())
                else:
                    header_df = self.build_header_df(msg, header_df)
                    headers = msg.headers()
                    dataframe_id = self.get_dataframe_id(headers)
                    value = msg.value()
                    try:
                        converter = self.get_converter_strategy(headers)
                        dataframe = converter.deserialize(value)

                        if dataframe_id not in dataframes:
                            dataframes[dataframe_id] = [dataframe]
                        else:
                            dataframes[dataframe_id].append(dataframe)

                    except Exception as e:
                        logging.error("Error processing message: %s", str(e))

        except KeyboardInterrupt:
            logging.info("KeyboardInterrupt: Consumer interrupted by user")

        except Exception as e:
            logging.error("Error in consumer: %s", str(e))
            raise e

        finally:
            consumer.close()
            logging.info("Consumer closed")

        # Add print statements to check the contents of the dataframes
        # dictionary
        logging.info(f"Dataframes dictionary: {dataframes}")
        result = []
        if header_df is not None:
            result.append(header_df)

        if len(dataframes) > 0:
            for dataframe_list in dataframes.values():
                combined_dataframe = pd.concat(
                    dataframe_list, ignore_index=True)
                result.append(combined_dataframe)

        return result
