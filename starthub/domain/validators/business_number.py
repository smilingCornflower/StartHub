from abc import ABC, abstractmethod

from domain.exceptions.validation import ValidationException
from domain.ports.validator import AbstractValidator


class BusinessNumberValidatorStrategy(AbstractValidator, ABC):
    @staticmethod
    @abstractmethod
    def validate(obj: str) -> None:
        """:raises ValidationException:"""
        pass


class KZBusinessNumberValidator(BusinessNumberValidatorStrategy):
    @staticmethod
    def validate(obj: str) -> None:
        """
        :raises ValidationException: if value is not 12 digits long or contains non-digit characters.
        """
        if not (len(obj) == 12 and obj.isdigit()):
            raise ValidationException("Invalid KZ business number")
