import uuid
from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, UUID4
from sqlalchemy import Column, String, DateTime, Enum, func, select, UUID, JSON, update
from sqlalchemy.orm import Session

from src.db.base import Base
from src.enums import EventStatus


class EventOutbox(Base):
    __tablename__ = 'event_outbox'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    event = Column(String, nullable=False)
    metadata_ = Column(JSON, nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    finished_at = Column(DateTime, nullable=True)
    status = Column(Enum(EventStatus), nullable=False)





