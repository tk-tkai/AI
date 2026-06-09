from typing import Literal

from pydantic import Field

from models.base import AppBaseModel


class CEODecisionModel(AppBaseModel):
    final_signal: Literal["BUY", "SELL", "HOLD"]
    confidence: int = Field(..., ge=0, le=100)
    entry: float = Field(..., gt=0)
    sl: float | None = Field(default=None, gt=0)  # 💡 ปรับให้เป็น None ได้เพื่อรองรับสัญญาณ HOLD
    tp: float | None = Field(default=None, gt=0)  # 💡 ปรับให้เป็น None ได้เพื่อรองรับสัญญาณ HOLD