from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from domain.models.base import BaseModel
from domain.value_objects import BaseVo
from domain.value_objects.common import OffsetPagination


class SearchParams(BaseVo):
    pass


T = TypeVar("T", bound=BaseModel)
S = TypeVar("S", bound=SearchParams)


class Search(ABC, Generic[S, T]):
    @abstractmethod
    def search(self, search_params: S, pagination: OffsetPagination) -> list[T]:
        pass
