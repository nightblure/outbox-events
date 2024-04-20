from datetime import datetime
from typing import Any

from pydantic import ConfigDict, BaseModel, UUID4

from src.enums import EventStatus


class EventOutboxRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID4
    event: str
    metadata_: dict[str, Any]
    created_at: datetime
    finished_at: datetime | None
    status: EventStatus


class EventOutboxCreate(BaseModel):
    event: str
    metadata_: dict[str, Any]
