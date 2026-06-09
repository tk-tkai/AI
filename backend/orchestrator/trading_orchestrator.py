from __future__ import annotations

import pandas as pd

from agents.ceo_agent import CEOAgent
from agents.chart_agent import ChartAgent
from agents.news_agent import NewsAgent
from agents.risk_agent import RiskAgent
from agents.sentiment_agent import SentimentAgent
from indicators.atr import calculate_atr
from config.logging_config import get_logger
from models.ceo_decision import CEODecisionModel
from models.paper_position import PaperPositionModel
from models.signal import SignalModel
from services.market_data_service import MarketDataService
from services.paper_trade_service import PaperTradeService
from services.signal_service import SignalService


class TradingOrchestrator:
    def __init__(self) -> None:
        self.logger = get_logger(self.__class__.__name__)

        self.market_data_service = MarketDataService()
        self.signal_service = SignalService()
        self.paper_trade_service = PaperTradeService()

        self.chart_agent = ChartAgent()
        self.news_agent = NewsAgent()
        self.sentiment_agent = SentimentAgent()
        self.risk_agent = RiskAgent()
        self.ceo_agent = CEOAgent()

    def generate_signal(
        self,
        symbol: str,
        timeframe: str,
        news_text: str,
    ) -> CEODecisionModel:
        self.logger.info(
            "Generating signal symbol=%s timeframe=%s",
            symbol,
            timeframe,
        )

        dataframe = self.market_data_service.get_market_data(
            symbol=symbol,
            interval=timeframe,
            limit=300,
        )

        chart_result = self.chart_agent.analyze(
            dataframe=dataframe,
        )

        news_result = self.news_agent.analyze(
            news_text=news_text,
        )

        sentiment_result = self.sentiment_agent.analyze(
            text=news_text,
        )

        latest_close = float(
            dataframe["close"].iloc[-1]
        )

        # ใช้ ATR จริง
        atr_series = calculate_atr(
            dataframe=dataframe,
            period=14,
        )

        atr = float(
            atr_series.iloc[-1]
        )

        if pd.isna(atr) or atr <= 0:
            self.logger.warning(
                "ATR invalid for %s. Using fallback.",
                symbol,
            )
            atr = latest_close * 0.005

        decision = self.ceo_agent.decide(
            chart_result=chart_result,
            news_result=news_result,
            sentiment_result=sentiment_result,
            entry=latest_close,
        )

        risk_result, sl, tp = self.risk_agent.analyze(
            signal=decision.final_signal,
            entry_price=latest_close,
            atr=atr,
        )

        decision.sl = sl
        decision.tp = tp

        self.logger.info(
            "Finalized decision symbol=%s signal=%s entry=%s sl=%s tp=%s",
            symbol,
            decision.final_signal,
            decision.entry,
            decision.sl,
            decision.tp,
        )

        signal = SignalModel(
            symbol=symbol,
            signal=decision.final_signal,
            confidence=decision.confidence,
            entry=decision.entry,
            sl=decision.sl,
            tp=decision.tp,
        )

        self.signal_service.save_signal(
            signal=signal,
        )

        # เปิด Paper Position อัตโนมัติ
        if decision.final_signal in [
            "BUY",
            "SELL",
        ]:
            try:
                paper_position = (
                    PaperPositionModel(
                        symbol=symbol,
                        side=decision.final_signal,
                        entry_price=decision.entry,
                        current_price=decision.entry,
                        sl=decision.sl,
                        tp=decision.tp,
                        status="OPEN",
                        quantity=1.0,
                    )
                )

                self.logger.info(
                    "OPEN TRADE symbol=%s side=%s entry=%s sl=%s tp=%s",
                    symbol,
                    decision.final_signal,
                    decision.entry,
                    decision.sl,
                    decision.tp,
                )

                self.paper_trade_service.open_position(
                    paper_position
                )

                self.logger.info(
                    "Successfully opened paper position for %s",
                    symbol,
                )

            except Exception as order_exc:
                self.logger.error(
                    "Failed to auto-open paper position symbol=%s error=%s",
                    symbol,
                    str(order_exc),
                )

        return decision