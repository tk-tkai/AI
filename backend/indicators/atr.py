from __future__ import annotations

import numpy as np
import pandas as pd


def calculate_atr(
    dataframe: pd.DataFrame,
    period: int = 14,
) -> pd.Series:
    high_low = dataframe["high"] - dataframe["low"]

    high_close = np.abs(
        dataframe["high"] - dataframe["close"].shift(1)
    )

    low_close = np.abs(
        dataframe["low"] - dataframe["close"].shift(1)
    )

    true_range = pd.concat(
        [
            high_low,
            high_close,
            low_close,
        ],
        axis=1,
    ).max(axis=1)

    atr = true_range.rolling(
        window=period,
        min_periods=period,
    ).mean()

    return atr