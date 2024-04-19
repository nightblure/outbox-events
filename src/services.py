from src.db.events_model import EventOutboxRepository
from src.events import BaseEvent, Event1, Event2


class EventPublisher:
    def __init__(self, *, event_outbox_repository: EventOutboxRepository):
        self.event_outbox_repository = event_outbox_repository

    def publish(self, event: BaseEvent):
        self.event_outbox_repository.register([event.to_outbox_event()])


class Service1(EventPublisher):
    def do_smth(self):
        metadata = dict(name='test', description='test', meta={'foo': 'bar'})
        e = Event1(metadata=metadata)
        self.publish(e)


class Service2(EventPublisher):
    def do_smth(self):
        e = Event2(data='Some second event data', field=22)
        self.publish(e)
