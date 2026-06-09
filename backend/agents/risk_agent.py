from __future__ import annotations

from typing import Literal

from config.logging_config import get_logger
from models.agent_result import AgentResultModel


class RiskAgent:
    def __init__(self) -> None:
        self.logger = get_logger(self.__class__.__name__)

    def analyze(
        self,
        signal: Literal["BUY", "SELL", "HOLD"],  # 💡 บังคับเป็น Literal เพื่อความปลอดภัย
        entry_price: float,
        atr: float,
    ) -> tuple[AgentResultModel, float, float]:
        self.logger.info("Calculating SL TP RR based on ATR")

        rr = 2.0

        if signal == "BUY":
            sl = entry_price - (atr * 1.5)
            tp = entry_price + ((entry_price - sl) * rr)

        elif signal == "SELL":
            sl = entry_price + (atr * 1.5)
            tp = entry_price - ((sl - entry_price) * rr)

        else:
            signal = "HOLD"
            sl = entry_price
            tp = entry_price

        result = AgentResultModel(
            agent="risk_agent",
            signal=signal,
            confidence=100,
            reasons=[
                f"RR={rr}",
                f"SL={round(sl, 4)}",  # ปัดเศษทศนิยมให้เก็บข้อมูลสะอาดขึ้น
                f"TP={round(tp, 4)}",
            ],
        )

        return result, sl, tp