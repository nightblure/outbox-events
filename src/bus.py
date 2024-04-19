from typing import Callable

from src.db.events_model import EventOutboxRepository
from src.events import BaseEvent


class EventsBus:
    def __init__(
            self,
            *,
            event_to_handler: dict[
                str,
                tuple[
                    type(BaseEvent), Callable[[BaseEvent], None]
                ]
            ],
            event_outbox_repository: EventOutboxRepository
    ):
        self.event_to_handler = event_to_handler
        self.event_outbox_repository = event_outbox_repository

    def handle_events(self):
        pending_events = self.event_outbox_repository.get_pending()

        for event_outbox in pending_events:
            event_type, handler = self.event_to_handler[event_outbox.event]
            event = event_type(**event_outbox.metadata_)
            handler(event)

        finished_event_ids = [e.id for e in pending_events]
        self.event_outbox_repository.set_status_finished(finished_event_ids)
