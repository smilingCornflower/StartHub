from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from application.ports.service import AbstractAppService

S = TypeVar("S", bound=AbstractAppService)


class AbstractServiceFactory(ABC, Generic[S]):
    @staticmethod
    @abstractmethod
    def create_service() -> S:
        pass
