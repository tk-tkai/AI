from __future__ import annotations

import pandas as pd


def calculate_rsi(
    dataframe: pd.DataFrame,
    period: int = 14,
    source_column: str = "close",
) -> pd.Series:
    delta = dataframe[source_column].diff()

    gain = delta.where(
        delta > 0,
        0.0,
    )

    loss = -delta.where(
        delta < 0,
        0.0,
    )

    average_gain = gain.rolling(
        window=period,
        min_periods=period,
    ).mean()

    average_loss = loss.rolling(
        window=period,
        min_periods=period,
    ).mean()

    rs = average_gain / average_loss

    rsi = 100 - (100 / (1 + rs))

    return rsi