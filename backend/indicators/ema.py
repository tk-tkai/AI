from __future__ import annotations

import pandas as pd


def calculate_ema(
    dataframe: pd.DataFrame,
    period: int,
    source_column: str = "close",
) -> pd.Series:
    return dataframe[source_column].ewm(
        span=period,
        adjust=False,
    ).mean()