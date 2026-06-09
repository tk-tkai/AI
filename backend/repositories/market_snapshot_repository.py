from models.market_snapshot import MarketSnapshotModel
from repositories.base_repository import BaseRepository


class MarketSnapshotRepository(BaseRepository):
    TABLE_NAME: str = "market_snapshots"

    def create_snapshot(
        self,
        snapshot: MarketSnapshotModel,
    ) -> dict:
        return self.insert(
            self.TABLE_NAME,
            snapshot.model_dump(mode="json"),  # 💡 แก้ไขตรงนี้ เติม mode="json" เพื่อเคลียร์บั๊ก datetime
        )

    def get_snapshots(self) -> list[dict]:
        return self.get_all(
            self.TABLE_NAME,
        )