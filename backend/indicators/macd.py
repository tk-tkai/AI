from __future__ import annotations

import pandas as pd


def calculate_macd(
    dataframe: pd.DataFrame,
    source_column: str = "close",
    fast_period: int = 12,
    slow_period: int = 26,
    signal_period: int = 9,
) -> pd.DataFrame:
    ema_fast = dataframe[source_column].ewm(
        span=fast_period,
        adjust=False,
    ).mean()

    ema_slow = dataframe[source_column].ewm(
        span=slow_period,
        adjust=False,
    ).mean()

    macd_line = ema_fast - ema_slow

    signal_line = macd_line.ewm(
        span=signal_period,
        adjust=False,
    ).mean()

    histogram = macd_line - signal_line

    return pd.DataFrame(
        {
            "macd": macd_line,
            "signal": signal_line,
            "histogram": histogram,
        }
    )