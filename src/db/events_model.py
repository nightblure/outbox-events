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


class EventOutboxRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_pending(self, *, limit: int = 100) -> list[EventOutboxRead]:
        stmt = (
            select(EventOutbox)
            .where(EventOutbox.status == EventStatus.pending)
            .limit(limit)
        )
        orm_events = self.db_session.scalars(stmt).all()
        return [EventOutboxRead.model_validate(e) for e in orm_events]

    def register(self, events: list[EventOutboxCreate]):
        orm_objects = [
            EventOutbox(
                metadata_=e.metadata_, event=e.event, status=EventStatus.pending
            ) for e in events
        ]
        self.db_session.add_all(orm_objects)
        self.db_session.commit()

    def set_status_finished(self, ids: list[uuid.uuid4]):
        stmt = (
            update(EventOutbox)
            .where(EventOutbox.id.in_(ids))
            .values(status=EventStatus.finished, finished_at=func.now())
        )
        self.db_session.execute(stmt)
        self.db_session.commit()
