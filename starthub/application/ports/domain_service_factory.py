from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from domain.ports.service import AbstractDomainService

S = TypeVar("S", bound=AbstractDomainService)


class AbstractDomainServiceFactory(ABC, Generic[S]):
    @staticmethod
    @abstractmethod
    def create_service() -> S:
        pass
