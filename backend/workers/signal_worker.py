from __future__ import annotations

from config.constants import SUPPORTED_SYMBOLS
from config.logging_config import get_logger
from config.settings import get_settings
from orchestrator.trading_orchestrator import (
    TradingOrchestrator,
)


class SignalWorker:
    def __init__(self) -> None:
        self.logger = get_logger(self.__class__.__name__)

        self.settings = get_settings()

        self.orchestrator = (
            TradingOrchestrator()
        )

    def run(
        self,
        news_text: str,
    ) -> None:
        self.logger.info(
            "SignalWorker started"
        )

        for symbol in SUPPORTED_SYMBOLS:
            try:
                decision = (
                    self.orchestrator
                    .generate_signal(
                        symbol=symbol,
                        timeframe=self.settings.DEFAULT_TIMEFRAME,
                        news_text=news_text,
                    )
                )

                self.logger.info(
                    "Signal generated symbol=%s signal=%s confidence=%s",
                    symbol,
                    decision.final_signal,
                    decision.confidence,
                )

            except Exception as exc:
                self.logger.error(
                    "SignalWorker failed symbol=%s error=%s",
                    symbol,
                    str(exc),
                )