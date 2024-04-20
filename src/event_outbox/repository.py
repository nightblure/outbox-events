from uuid import uuid4

from sqlalchemy import select, update, func
from sqlalchemy.orm import Session

from src.enums import EventStatus
from src.event_outbox.model import EventOutbox
from src.event_outbox.schemas import EventOutboxRead, EventOutboxCreate


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

    def set_status_finished(self, ids: list[uuid4]):
        stmt = (
            update(EventOutbox)
            .where(EventOutbox.id.in_(ids))
            .values(status=EventStatus.finished, finished_at=func.now())
        )
        self.db_session.execute(stmt)
        self.db_session.commit()
