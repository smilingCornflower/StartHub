from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from domain.enums.event import EventTypeEnum
from domain.value_objects import BaseVo


class AbstractEvent(ABC, BaseVo):
    pass


E = TypeVar("E", bound=AbstractEvent)


class AbstractEventHandler(ABC):
    @abstractmethod
    def handle(self, event: E) -> None:
        pass

    @abstractmethod
    def get_event_type(self) -> EventTypeEnum:
        pass


H = TypeVar("H", bound=AbstractEventHandler)


class AbstractEventBus(ABC, Generic[E]):
    @abstractmethod
    def subscribe(self, event_type: EventTypeEnum, handler: H) -> None:
        pass

    @abstractmethod
    def publish(self, event: E) -> None:
        pass
