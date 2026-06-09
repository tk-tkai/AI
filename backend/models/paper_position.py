from datetime import datetime, UTC
from typing import Literal
from uuid import uuid4

from pydantic import Field

from models.base import AppBaseModel


class PaperPositionModel(AppBaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    symbol: str
    side: Literal["BUY", "SELL"]
    entry_price: float = Field(..., gt=0)
    current_price: float = Field(..., gt=0)
    sl: float = Field(..., gt=0)
    tp: float = Field(..., gt=0)
    quantity: float = Field(..., gt=0)
    status: Literal["OPEN", "CLOSED"] = "OPEN"
    opened_at: datetime = Field(default_factory=lambda: datetime.now(UTC))  # 💡 ใช้ datetime.now(UTC) แทน utcnow
    closed_at: datetime | None = None