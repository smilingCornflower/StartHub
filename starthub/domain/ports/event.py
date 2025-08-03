from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from domain.enums.event import AnyEventType
from domain.value_objects import BaseVo


class AbstractEvent(ABC, BaseVo):
    event_type: AnyEventType


E = TypeVar("E", bound=AbstractEvent)


class AbstractEventHandler(ABC, Generic[E]):
    @abstractmethod
    def handle(self, event: E) -> None:
        pass


class AbstractEventBus(ABC):
    @abstractmethod
    def subscribe(self, event_type: AnyEventType, handler: AbstractEventHandler[AbstractEvent]) -> None:
        pass

    @abstractmethod
    def publish(self, event: AbstractEvent) -> None:
        pass
