from __future__ import annotations

import pandas as pd

from indicators.adx import calculate_adx
from indicators.atr import calculate_atr
from indicators.bollinger import calculate_bollinger_bands
from indicators.ema import calculate_ema
from indicators.macd import calculate_macd
from indicators.rsi import calculate_rsi


def build_indicator_bundle(
    dataframe: pd.DataFrame,
) -> pd.DataFrame:
    dataframe = dataframe.copy()

    dataframe["ema20"] = calculate_ema(
        dataframe,
        period=20,
    )

    dataframe["ema50"] = calculate_ema(
        dataframe,
        period=50,
    )

    dataframe["rsi"] = calculate_rsi(
        dataframe,
    )

    macd = calculate_macd(
        dataframe,
    )

    dataframe["macd"] = macd["macd"]
    dataframe["macd_signal"] = macd["signal"]
    dataframe["macd_histogram"] = macd["histogram"]

    dataframe["atr"] = calculate_atr(
        dataframe,
    )

    adx = calculate_adx(
        dataframe,
    )

    dataframe["adx"] = adx["adx"]
    dataframe["plus_di"] = adx["plus_di"]
    dataframe["minus_di"] = adx["minus_di"]

    bb = calculate_bollinger_bands(
        dataframe,
    )

    dataframe["bb_upper"] = bb["upper_band"]
    dataframe["bb_middle"] = bb["middle_band"]
    dataframe["bb_lower"] = bb["lower_band"]

    return dataframe