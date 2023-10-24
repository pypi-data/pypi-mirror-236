from abc import abstractmethod
from typing import Any

import pandas as pd


class BaseDataFrameConvertor:
    @abstractmethod
    def convert(df: pd.DataFrame) -> Any:
        pass

    @abstractmethod
    def serialize(df: pd.DataFrame) -> Any:
        pass

    @abstractmethod
    def deserialize(input: Any) -> pd.DataFrame:
        pass
