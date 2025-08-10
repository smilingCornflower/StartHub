from domain.enums.event import AnyEventType
from domain.ports.event import AbstractEvent


class DomainEvent(AbstractEvent):
    event_type: AnyEventType

    class Config:
        arbitrary_types_allowed = True
