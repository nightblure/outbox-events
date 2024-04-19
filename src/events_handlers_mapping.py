from src.event_names import EVENT1_NAME, EVENT2_NAME
from src.events import Event1, Event2
from src.handlers import e1_handler, e2_handler

event_to_handler = {
    EVENT1_NAME: (Event1, e1_handler),
    EVENT2_NAME: (Event2, e2_handler),
}
