# KafkaDataFrames

# What is it?

Qurix kafka dataframes is a Python package that provides a class for sending Pandas DataFrames as required format(e.g. JSON, AVRO etc) to confluent Kafka. It simplifies the process of splitting DataFrames into batches and sending them as individual messages to Kafka topics. This README provides an overview of the package and instructions for usage.

# Main Features

Key features of the package include:

- Producing and consuming the messages using confluent kafka platform
- DataFrame to JSON/AVRO Conversion: The package provides a method (`convert()`)uses to convert pandas DataFrames into JSON and AVRO formats, respectively.
- Batch Sending: The package allows users to send DataFrame data to Kafka in batches, dividing the JSON or AVRO data into smaller chunks for efficient processing.
-Enums : To choose between message formats enums are introduced and can used by importing the `message_formats` module
- Kafka Metadata Headers: For each batch sent to Kafka, metadata headers such as `dataframe_id`, `dataframe_name`, `batch_num`, and `total_batches` are attached, providing additional context to consumers.
- Logging: The package sets up logging using the Python `logging` module to facilitate monitoring and error handling during execution.

# Requirements

`pandas`
`confluent-kafka`
`fastavro`

You can install these dependencies manually or use the provided requirements.txt file in repository.


# Installation

## Create a new virtual environment
`python -m virtualenv .venv --python="python3.11"`

## Activate
source .venv/bin/activate

## Install
To install the `qurix-kafka-dataframes` package, you can use `pip`:

`pip install qurix-kafka-dataframes`

# Usage

Import the `DataFrameProducer` class from the package:
`from qurix.kafka.dataframes.dataframe_producer import JsonDataFrameProducer`

## Example to use Producer
```
from qurix.kafka.dataframes.dataframe_producer import JsonDataFrameProducer
from qurix.kafka.dataframes.message_formats import MessageFormat
import pandas as pd

#Create a DataFrame
data = {'Name': ['John', 'Jane', 'Mike'],'Age': [25, 30, 35]}
df = pd.DataFrame(data)

#Kafka topic to send the data
kafka_topic = 'my_topic'

#Configuration for Kafka producer
kafka_conf = {'bootstrap.servers': 'my server', 'client.id': 'my_name'}

#Create an instance of DataFrameProducer
producer = DataFrameProducer(kafka_conf, MessageFormat.JSON)

#Send the DataFrame to Kafka
producer.send_dataframe(df, kafka_topic)

```

## Example to use Consumer

```
from qurix.kafka.dataframes.dataframe_consumer import DataFrameConsumer
from qurix.kafka.dataframes.message_formats import MessageFormat

#Configuration for Kafka
conf = {'bootstrap.servers': 'localhost:9092','group.id': 'my_consumer_group', 'auto.offset.reset': 'earliest' }

#Kafka-Topic and Consumer
kafka_topic = 'my_topic'

#Create consumer instance
consumer = DataFrameConsumer(conf)

#Consume msgs for topic
result = consumer.consume_dataframes(kafka_topic)

#Get result
header_dataframe = result[0] # Header-DataFrame
dataframe = result[1] 
print(dataframe)

```

# Contact
For any inquiries or questions, feel free to reach out

