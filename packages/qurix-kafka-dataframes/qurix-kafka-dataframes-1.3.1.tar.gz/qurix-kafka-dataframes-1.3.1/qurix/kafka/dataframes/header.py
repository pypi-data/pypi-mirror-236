import datetime
from dataclasses import dataclass

import pandas as pd


@dataclass
class HeadersGenerator:
    format_type: str
    transaction_id: str
    source: str
    target: str
    dataflow_id: str
    dataflow_name: str
    batch_number: str
    batch_size: str
    records: str
    data_container_id: str
    creation_time: datetime = pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
