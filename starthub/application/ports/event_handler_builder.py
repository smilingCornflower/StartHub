from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from domain.ports.event import AbstractEvent, AbstractEventHandler

H = TypeVar("H", bound=AbstractEventHandler[AbstractEvent])


class AbstractEventHandlerBuilder(ABC, Generic[H]):
    @staticmethod
    @abstractmethod
    def create_handler() -> H:
        pass
