from __future__ import annotations

from typing import Any

import pandas as pd

from config.logging_config import get_logger
from providers.provider_factory import ProviderFactory


class MarketDataService:
    def __init__(self) -> None:
        self.logger = get_logger(self.__class__.__name__)

    def get_market_data(
        self,
        symbol: str,
        interval: str,
        limit: int = 500,
    ) -> pd.DataFrame:
        self.logger.info(
            "Fetching market data symbol=%s interval=%s",
            symbol,
            interval,
        )

        provider = ProviderFactory.get_provider(symbol)

        return provider.get_ohlcv(
            symbol=symbol,
            interval=interval,
            limit=limit,
        )

    def get_latest_price(
        self,
        symbol: str,
    ) -> float:
        provider = ProviderFactory.get_provider(symbol)

        return provider.get_latest_price(symbol)