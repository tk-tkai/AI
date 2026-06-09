from __future__ import annotations

from config.logging_config import get_logger
from models.paper_trade import PaperTradeModel
from services.paper_trade_service import (
    PaperTradeService,
)
from services.performance_service import (
    PerformanceService,
)


class PerformanceOrchestrator:
    def __init__(self) -> None:
        self.logger = get_logger(
            self.__class__.__name__
        )

        self.paper_trade_service = (
            PaperTradeService()
        )

        self.performance_service = (
            PerformanceService()
        )

    def calculate_and_store(
        self,
        trades: list[PaperTradeModel],
        balance: float,
        equity: float,
    ) -> dict:
        stats = (
            self.paper_trade_service
            .calculate_performance(
                trades=trades,
                balance=balance,
                equity=equity,
            )
        )

        return self.performance_service.save_stats(
            stats
        )