from abc import ABC, abstractmethod

from domain.models.project_management.funding_model import FundingModel
from domain.ports.repository import AbstractReadRepository
from domain.value_objects.common import CursorPagination, Id, OffsetPagination
from domain.value_objects.filter import FundingModelFilter


class FundingModelReadRepository(AbstractReadRepository[FundingModel, FundingModelFilter, Id], ABC):
    @abstractmethod
    def get_by_id(self, id_: Id) -> FundingModel:
        """:raises FundingModelNotFoundException:"""
        pass

    @abstractmethod
    def get_all(
        self, filter_: FundingModelFilter, pagination: CursorPagination | OffsetPagination | None = None
    ) -> list[FundingModel]:
        pass
