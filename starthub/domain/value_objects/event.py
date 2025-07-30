from datetime import datetime
from typing import Any

from domain.enums.event import EventTypeEnum
from domain.ports.event import AbstractEvent
from domain.value_objects.common import Id, Uuid


class DomainEvent(AbstractEvent):
    event_id: Uuid
    aggregate_id: Id
    event_type: EventTypeEnum
    occured_on: datetime
    payload: dict[str, Any]
    version: int = 1
