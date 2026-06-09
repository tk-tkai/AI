from pydantic import Field

from models.base import AppBaseModel
from models.paper_position import PaperPositionModel
from models.paper_trade import PaperTradeModel


class PaperAccountModel(AppBaseModel):
    balance: float = Field(default=60.0, gt=0)
    equity: float = Field(default=60.0, gt=0)
    open_positions: list[PaperPositionModel] = Field(default_factory=list)
    closed_positions: list[PaperPositionModel] = Field(default_factory=list)
    trades: list[PaperTradeModel] = Field(default_factory=list)