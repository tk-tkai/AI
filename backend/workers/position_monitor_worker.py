from __future__ import annotations

from config.logging_config import get_logger
from models.paper_position import PaperPositionModel
from orchestrator.paper_trading_orchestrator import (
    PaperTradingOrchestrator,
)
from repositories.paper_positions_repository import (
    PaperPositionsRepository,
)


class PositionMonitorWorker:
    def __init__(self) -> None:
        self.logger = get_logger(
            self.__class__.__name__
        )

        self.repository = (
            PaperPositionsRepository()
        )

        self.orchestrator = (
            PaperTradingOrchestrator()
        )

    def run(self) -> None:
        self.logger.info(
            "PositionMonitorWorker started"
        )

        positions = (
            self.repository.get_positions()
        )

        for item in positions:
            try:
                if item["status"] != "OPEN":
                    continue

                position = (
                    PaperPositionModel(
                        **item
                    )
                )

                self.orchestrator.monitor_position(
                    position
                )

            except Exception as exc:
                self.logger.error(
                    "Position monitor error position=%s error=%s",
                    item.get("id"),
                    str(exc),
                )