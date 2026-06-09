from models.performance_stats import PerformanceStatsModel
from repositories.base_repository import BaseRepository


class PerformanceStatsRepository(BaseRepository):
    TABLE_NAME: str = "performance_stats"

    def save_stats(
        self,
        stats: PerformanceStatsModel,
    ) -> dict:
        return self.insert(
            self.TABLE_NAME,
            stats.model_dump(),
        )

    def get_stats(self) -> list[dict]:
        return self.get_all(
            self.TABLE_NAME,
        )