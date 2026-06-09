from __future__ import annotations

from config.logging_config import get_logger
from models.paper_trade import PaperTradeModel
from orchestrator.performance_orchestrator import (
    PerformanceOrchestrator,
)
from repositories.paper_trades_repository import (
    PaperTradesRepository,
)


class PerformanceWorker:
    def __init__(self) -> None:
        self.logger = get_logger(
            self.__class__.__name__
        )

        self.repository = (
            PaperTradesRepository()
        )

        self.orchestrator = (
            PerformanceOrchestrator()
        )

    def run(
        self,
        balance: float,
        equity: float,
    ) -> None:
        self.logger.info(
            "PerformanceWorker started"
        )

        trades_data = (
            self.repository.get_trades()
        )

        trades = [
            PaperTradeModel(**trade)
            for trade in trades_data
        ]

        self.orchestrator.calculate_and_store(
            trades=trades,
            balance=balance,
            equity=equity,
        )