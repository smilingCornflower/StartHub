from abc import ABC, abstractmethod

from domain.models.project_management.funding_model import FundingModel
from domain.ports.repository import AbstractReadRepository, AbstractWriteRepository
from domain.value_objects.common import CursorPagination, OffsetPagination
from domain.value_objects.filter import FundingModelFilter
from domain.value_objects.project.funding_model import (
    FundingModelCreatePayload,
    FundingModelId,
    FundingModelUpdatePayload,
)


class FundingModelReadRepository(AbstractReadRepository[FundingModel, FundingModelFilter, FundingModelId], ABC):
    @abstractmethod
    def get_by_id(self, id_: FundingModelId) -> FundingModel:
        """:raises FundingModelNotFoundException:"""
        pass

    @abstractmethod
    def get_all(
        self, filter_: FundingModelFilter, pagination: CursorPagination | OffsetPagination | None = None
    ) -> list[FundingModel]:
        pass


class FundingModelWriteRepository(
    AbstractWriteRepository[FundingModel, FundingModelCreatePayload, FundingModelUpdatePayload, FundingModelId], ABC
):
    @abstractmethod
    def create(self, data: FundingModelCreatePayload) -> FundingModel:
        pass

    @abstractmethod
    def update(self, data: FundingModelUpdatePayload) -> FundingModel:
        pass

    @abstractmethod
    def delete_by_id(self, id_: FundingModelId) -> None:
        pass
