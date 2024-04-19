from src.db.deps import get_db_session_context

from src.deps import create_events_bus


def outbox_events_task():
    with get_db_session_context() as db_session:
        bus = create_events_bus(db_session)
        bus.handle_events()
