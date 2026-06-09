from __future__ import annotations

import logging
from typing import Any

import pandas as pd
import requests

from config.settings import get_settings
from providers.base_provider import BaseProvider


class BinanceProvider(BaseProvider):
    def __init__(self) -> None:
        settings = get_settings()

        self.base_url: str = settings.BINANCE_BASE_URL
        self.logger = logging.getLogger(self.__class__.__name__)

    def get_ohlcv(
        self,
        symbol: str,
        interval: str,
        limit: int = 500,
    ) -> pd.DataFrame:
        url = f"{self.base_url}/api/v3/klines"

        params: dict[str, Any] = {
            "symbol": symbol,
            "interval": interval,
            "limit": limit,
        }

        response = requests.get(
            url=url,
            params=params,
            timeout=30,
        )

        response.raise_for_status()

        data = response.json()

        dataframe = pd.DataFrame(
            data,
            columns=[
                "open_time",
                "open",
                "high",
                "low",
                "close",
                "volume",
                "close_time",
                "quote_asset_volume",
                "number_of_trades",
                "taker_buy_base_asset_volume",
                "taker_buy_quote_asset_volume",
                "ignore",
            ],
        )

        dataframe["open"] = dataframe["open"].astype(float)
        dataframe["high"] = dataframe["high"].astype(float)
        dataframe["low"] = dataframe["low"].astype(float)
        dataframe["close"] = dataframe["close"].astype(float)
        dataframe["volume"] = dataframe["volume"].astype(float)

        return dataframe

    def get_latest_price(
        self,
        symbol: str,
    ) -> float:
        url = f"{self.base_url}/api/v3/ticker/price"

        response = requests.get(
            url=url,
            params={"symbol": symbol},
            timeout=30,
        )

        response.raise_for_status()

        payload = response.json()

        return float(payload["price"])