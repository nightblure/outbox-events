from src.bus import EventsBus
from src.event_outbox.repository import EventOutboxRepository
from src.events_handlers_mapping import event_to_handler
from src.scheduler import TasksScheduler
from src.services import Service1, Service2


def create_event_outbox_repository(db_session):
    return EventOutboxRepository(db_session)


def create_events_bus(db_session):
    return EventsBus(
        event_to_handler=event_to_handler,
        event_outbox_repository=create_event_outbox_repository(db_session)
    )


def create_service1(db_session):
    return Service1(
        event_outbox_repository=create_event_outbox_repository(db_session)
    )


def create_service2(db_session):
    return Service2(
        event_outbox_repository=create_event_outbox_repository(db_session)
    )


def create_tasks_scheduler():
    return TasksScheduler()
