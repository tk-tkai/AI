from __future__ import annotations

import logging

import pandas as pd
import yfinance as yf

from providers.base_provider import BaseProvider


class YFinanceProvider(BaseProvider):
    INTERVAL_MAP: dict[str, str] = {
        "15m": "15m",
        "1h": "60m",
        "4h": "1h",
        "1d": "1d",
    }

    def __init__(self) -> None:
        self.logger = logging.getLogger(
            self.__class__.__name__
        )

    def get_ohlcv(
        self,
        symbol: str,
        interval: str,
        limit: int = 500,
    ) -> pd.DataFrame:
        yf_interval = self.INTERVAL_MAP.get(
            interval,
            "15m",
        )

        dataframe = yf.download(
            tickers=symbol,
            period="60d",
            interval=yf_interval,
            progress=False,
            auto_adjust=False,
            threads=False,
        )

        if dataframe.empty:
            raise ValueError(
                f"No market data returned for {symbol}"
            )

        dataframe = dataframe.tail(limit)

        # Fix MultiIndex columns from yfinance
        if isinstance(
            dataframe.columns,
            pd.MultiIndex,
        ):
            dataframe.columns = (
                dataframe.columns.get_level_values(0)
            )

        dataframe = dataframe.rename(
            columns={
                "Open": "open",
                "High": "high",
                "Low": "low",
                "Close": "close",
                "Volume": "volume",
            }
        )

        required_columns = [
            "open",
            "high",
            "low",
            "close",
            "volume",
        ]

        missing_columns = [
            col
            for col in required_columns
            if col not in dataframe.columns
        ]

        if missing_columns:
            raise ValueError(
                f"Missing columns for {symbol}: "
                f"{missing_columns}"
            )

        dataframe = dataframe[
            required_columns
        ]

        self.logger.info(
            "Processed columns for %s: %s",
            symbol,
            dataframe.columns.tolist(),
        )

        return dataframe

    def get_latest_price(
        self,
        symbol: str,
    ) -> float:
        ticker = yf.Ticker(symbol)

        history = ticker.history(
            period="1d",
            interval="1m",
        )

        if history.empty:
            raise ValueError(
                f"No price data returned for {symbol}"
            )

        return float(
            history["Close"].iloc[-1]
        )