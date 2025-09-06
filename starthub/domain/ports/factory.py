from abc import ABC, abstractmethod
from typing import Any


class Factory(ABC):
    @staticmethod
    @abstractmethod
    def create() -> Any:
        pass
