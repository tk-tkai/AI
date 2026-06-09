from config.logging_config import get_logger
from models.market_snapshot import MarketSnapshotModel
from repositories.market_snapshot_repository import MarketSnapshotRepository


class MarketSnapshotService:
    def __init__(self) -> None:
        self.logger = get_logger(self.__class__.__name__)
        self.repository = MarketSnapshotRepository()

    def save_snapshot(
        self,
        snapshot: MarketSnapshotModel,
    ) -> dict | None:  # 💡 ปรับ Type Hint ให้รองรับ None เผื่อกรณีที่บันทึกไม่สำเร็จ
        self.logger.info(
            "Saving market snapshot for symbol=%s, timeframe=%s, close=%s",
            snapshot.symbol,
            snapshot.timeframe,
            snapshot.close_price,
        )

        try:
            # ส่งโมเดลไปให้ Repository จัดการบันทึก
            return self.repository.create_snapshot(snapshot)
        except Exception as exc:
            # 💡 ดักจับ Error ป้องกันไม่ให้ Data Ingestion Pipeline พังหยุดทำงานกลางคัน
            self.logger.error(
                "Failed to save market snapshot for symbol=%s, timeframe=%s. Error: %s",
                snapshot.symbol,
                snapshot.timeframe,
                str(exc),
            )
            return None