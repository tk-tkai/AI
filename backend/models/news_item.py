from datetime import UTC, datetime, UTC

from pydantic import Field

from models.base import AppBaseModel


class NewsItemModel(AppBaseModel):
    title: str
    source: str
    url: str
    summary: str
    published_at: datetime = Field(default_factory=lambda: datetime.now(UTC))