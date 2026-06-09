from datetime import datetime, UTC
from typing import Literal
from uuid import uuid4

from pydantic import Field

from models.base import AppBaseModel


class PaperTradeModel(AppBaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    position_id: str
    symbol: str
    side: Literal["BUY", "SELL"]
    entry_price: float
    exit_price: float
    quantity: float
    pnl: float
    rr: float
    result: Literal["WIN", "LOSS", "BREAKEVEN"]
    opened_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    closed_at: datetime = Field(default_factory=lambda: datetime.now(UTC))