from config.logging_config import get_logger
from models.performance_stats import PerformanceStatsModel
from repositories.performance_stats_repository import (
    PerformanceStatsRepository,
)


class PerformanceService:
    def __init__(self) -> None:
        self.logger = get_logger(self.__class__.__name__)
        self.repository = PerformanceStatsRepository()

    def save_stats(
        self,
        stats: PerformanceStatsModel,
    ) -> dict:
        self.logger.info("Saving performance stats")

        return self.repository.save_stats(stats)

    def get_stats(self) -> list[dict]:
        return self.repository.get_stats()