from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from domain.ports.event import AbstractEvent

E = TypeVar("E", bound=AbstractEvent)


class AbstractAggregateRoot(ABC, Generic[E]):
    @abstractmethod
    def add_domain_event(self, event: E) -> None:
        pass

    @abstractmethod
    def get_domain_events(self) -> list[E]:
        pass

    @abstractmethod
    def clear_domain_events(self) -> None:
        pass
