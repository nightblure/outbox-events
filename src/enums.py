from enum import Enum, auto


class EventStatus(str, Enum):
    pending = auto()
    finished = auto()
