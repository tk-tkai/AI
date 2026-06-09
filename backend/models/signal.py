from typing import Literal

from pydantic import Field

from models.base import AppBaseModel


class SignalModel(AppBaseModel):
    symbol: str = Field(..., min_length=3)
    signal: Literal["BUY", "SELL", "HOLD"]
    confidence: int = Field(..., ge=0, le=100)
    entry: float = Field(..., gt=0)
    sl: float = Field(..., gt=0)
    tp: float = Field(..., gt=0)