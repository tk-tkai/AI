from __future__ import annotations

import numpy as np
import pandas as pd


def calculate_adx(
    dataframe: pd.DataFrame,
    period: int = 14,
) -> pd.DataFrame:
    high = dataframe["high"]
    low = dataframe["low"]
    close = dataframe["close"]

    plus_dm = high.diff()

    minus_dm = -low.diff()

    plus_dm = plus_dm.where(
        (plus_dm > minus_dm) & (plus_dm > 0),
        0.0,
    )

    minus_dm = minus_dm.where(
        (minus_dm > plus_dm) & (minus_dm > 0),
        0.0,
    )

    tr1 = high - low

    tr2 = np.abs(
        high - close.shift(1)
    )

    tr3 = np.abs(
        low - close.shift(1)
    )

    true_range = pd.concat(
        [tr1, tr2, tr3],
        axis=1,
    ).max(axis=1)

    atr = true_range.rolling(
        period,
    ).mean()

    plus_di = (
        100
        * (
            plus_dm.rolling(period).mean()
            / atr
        )
    )

    minus_di = (
        100
        * (
            minus_dm.rolling(period).mean()
            / atr
        )
    )

    dx = (
        (
            abs(
                plus_di - minus_di
            )
            /
            (
                plus_di + minus_di
            )
        )
        * 100
    )

    adx = dx.rolling(
        period,
    ).mean()

    return pd.DataFrame(
        {
            "adx": adx,
            "plus_di": plus_di,
            "minus_di": minus_di,
        }
    )