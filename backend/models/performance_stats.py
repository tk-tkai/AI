from pydantic import Field

from models.base import AppBaseModel


class PerformanceStatsModel(AppBaseModel):
    equity: float = Field(..., ge=0)
    balance: float = Field(..., ge=0)
    win_rate: float = Field(..., ge=0)
    profit_factor: float = Field(..., ge=0)
    total_trades: int = Field(..., ge=0)
    average_rr: float
    max_drawdown: float = Field(..., ge=0)