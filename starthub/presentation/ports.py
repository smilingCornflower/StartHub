from abc import ABC, abstractmethod

from rest_framework.response import Response


class ErrorResponseFactory(ABC):
    @classmethod
    @abstractmethod
    def create_response(cls, exception: Exception) -> Response:
        pass
