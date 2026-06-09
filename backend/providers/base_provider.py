from abc import ABC, abstractmethod

import pandas as pd


class BaseProvider(ABC):
    @abstractmethod
    def get_ohlcv(
        self,
        symbol: str,
        interval: str,
        limit: int = 500,
    ) -> pd.DataFrame:
        raise NotImplementedError

    @abstractmethod
    def get_latest_price(
        self,
        symbol: str,
    ) -> float:
        raise NotImplementedError