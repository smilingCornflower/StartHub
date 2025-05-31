from abc import ABC, abstractmethod
from typing import Any


class AbstractValidator(ABC):
    @staticmethod
    @abstractmethod
    def validate(obj: Any) -> None:
        """:raises ValidationException:"""
        # domain.exception.validation.ValidationException
        pass
