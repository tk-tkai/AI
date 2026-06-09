from datetime import datetime, UTC

from pydantic import Field

from models.base import AppBaseModel


class MarketSnapshotModel(AppBaseModel):
    symbol: str
    timeframe: str
    open_price: float
    high_price: float
    low_price: float
    close_price: float
    volume: float
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))