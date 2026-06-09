from __future__ import annotations

import pandas as pd

from config.logging_config import get_logger
from indicators.indicator_bundle import build_indicator_bundle
from models.agent_result import AgentResultModel


class ChartAgent:
    def __init__(self) -> None:
        self.logger = get_logger(self.__class__.__name__)

    def analyze(
        self,
        dataframe: pd.DataFrame,
    ) -> AgentResultModel:
        self.logger.info("Running chart analysis")

        df = build_indicator_bundle(dataframe)

        latest = df.iloc[-1]

        bullish_score = 0
        bearish_score = 0
        reasons: list[str] = []

        if latest["ema20"] > latest["ema50"]:
            bullish_score += 1
            reasons.append("EMA20 above EMA50")
        else:
            bearish_score += 1
            reasons.append("EMA20 below EMA50")

        if latest["macd"] > latest["macd_signal"]:
            bullish_score += 1
            reasons.append("MACD bullish crossover")
        else:
            bearish_score += 1
            reasons.append("MACD bearish crossover")

        if latest["rsi"] < 30:
            bullish_score += 1
            reasons.append("RSI oversold")

        if latest["rsi"] > 70:
            bearish_score += 1
            reasons.append("RSI overbought")

        if latest["adx"] > 25:
            reasons.append("Strong trend ADX")

        if latest["close"] < latest["bb_lower"]:
            bullish_score += 1
            reasons.append("Price below lower Bollinger Band")

        if latest["close"] > latest["bb_upper"]:
            bearish_score += 1
            reasons.append("Price above upper Bollinger Band")

        if bullish_score > bearish_score:
            signal = "BUY"
            confidence = min(
                100,
                50 + ((bullish_score - bearish_score) * 10),
            )
        elif bearish_score > bullish_score:
            signal = "SELL"
            confidence = min(
                100,
                50 + ((bearish_score - bullish_score) * 10),
            )
        else:
            signal = "HOLD"
            confidence = 50

        return AgentResultModel(
            agent="chart_agent",
            signal=signal,
            confidence=confidence,
            reasons=reasons,
        )