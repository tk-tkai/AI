from typing import List, Literal

from pydantic import Field

from models.base import AppBaseModel


class AgentResultModel(AppBaseModel):
    agent: str = Field(..., min_length=2)
    signal: Literal["BUY", "SELL", "HOLD"]
    confidence: int = Field(..., ge=0, le=100)
    reasons: List[str] = Field(default_factory=list)