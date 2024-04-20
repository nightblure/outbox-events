from dataclasses import dataclass
from typing import Protocol

from src.event_outbox.schemas import EventOutboxCreate
from src.event_names import EVENT1_NAME, EVENT2_NAME


class BaseEvent(Protocol):
    name: str

    def to_outbox_event(self) -> EventOutboxCreate:
        pass


@dataclass
class Event1:
    metadata: dict
    name: str = EVENT1_NAME

    def to_outbox_event(self):
        return EventOutboxCreate(event=self.name, metadata_={'metadata': self.metadata})


@dataclass
class Event2:
    data: str
    field: int
    name: str = EVENT2_NAME

    def to_outbox_event(self):
        metadata = dict(field=self.field, data=self.data)
        return EventOutboxCreate(event=self.name, metadata_=metadata)
