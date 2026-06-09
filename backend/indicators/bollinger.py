from __future__ import annotations

import pandas as pd


def calculate_bollinger_bands(
    dataframe: pd.DataFrame,
    period: int = 20,
    deviation: float = 2.0,
    source_column: str = "close",
) -> pd.DataFrame:
    middle_band = dataframe[
        source_column
    ].rolling(
        window=period,
    ).mean()

    standard_deviation = dataframe[
        source_column
    ].rolling(
        window=period,
    ).std()

    upper_band = (
        middle_band
        + deviation
        * standard_deviation
    )

    lower_band = (
        middle_band
        - deviation
        * standard_deviation
    )

    return pd.DataFrame(
        {
            "upper_band": upper_band,
            "middle_band": middle_band,
            "lower_band": lower_band,
        }
    )