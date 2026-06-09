from datetime import datetime
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field


class AppBaseModel(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
        extra="forbid",
        from_attributes=True,
    )


class TimestampMixin(AppBaseModel):
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class UUIDMixin(AppBaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))