from __future__ import annotations

from config.constants import SUPPORTED_SYMBOLS
from config.logging_config import get_logger
from config.settings import get_settings
from models.market_snapshot import MarketSnapshotModel
from services.market_data_service import MarketDataService
from services.market_snapshot_service import (
    MarketSnapshotService,
)


class MarketDataWorker:
    def __init__(self) -> None:
        self.logger = get_logger(self.__class__.__name__)

        self.settings = get_settings()

        self.market_data_service = (
            MarketDataService()
        )

        self.snapshot_service = (
            MarketSnapshotService()
        )

    def run(self) -> None:
        self.logger.info(
            "MarketDataWorker started"
        )

        for symbol in SUPPORTED_SYMBOLS:
            try:
                dataframe = (
                    self.market_data_service
                    .get_market_data(
                        symbol=symbol,
                        interval=self.settings.DEFAULT_TIMEFRAME,
                        limit=1,
                    )
                )

                latest = dataframe.iloc[-1]

                snapshot = MarketSnapshotModel(
                    symbol=symbol,
                    timeframe=self.settings.DEFAULT_TIMEFRAME,
                    open_price=float(latest["open"]),
                    high_price=float(latest["high"]),
                    low_price=float(latest["low"]),
                    close_price=float(latest["close"]),
                    volume=float(latest["volume"]),
                )

                self.snapshot_service.save_snapshot(
                    snapshot
                )

                self.logger.info(
                    "Snapshot stored symbol=%s",
                    symbol,
                )

            except Exception as exc:
                self.logger.error(
                    "MarketDataWorker failed symbol=%s error=%s",
                    symbol,
                    str(exc),
                )