from abc import ABC, abstractmethod

from domain.models.company import Company, CompanyFounder
from domain.ports.repository import AbstractReadRepository, AbstractWriteRepository
from domain.value_objects.common import Id, Pagination
from domain.value_objects.company import (
    CompanyCreatePayload,
    CompanyFounderCreatePayload,
    CompanyFounderUpdatePayload,
    CompanyUpdatePayload,
)
from domain.value_objects.filter import CompanyFilter, CompanyFounderFilter


class CompanyReadRepository(AbstractReadRepository[Company, CompanyFilter], ABC):
    @abstractmethod
    def get_by_id(self, id_: Id) -> Company:
        """:raises CompanyNotFoundException:"""
        pass

    @abstractmethod
    def get_all(self, filter_: CompanyFilter, pagination: Pagination | None = None) -> list[Company]:
        pass

    @abstractmethod
    def get_by_project_id(self, id_: Id) -> Company:
        """:raises CompanyNotFoundException:"""
        pass


class CompanyWriteRepository(AbstractWriteRepository[Company, CompanyCreatePayload, CompanyUpdatePayload], ABC):
    @abstractmethod
    def create(self, data: CompanyCreatePayload) -> Company:
        pass

    @abstractmethod
    def update(self, data: CompanyUpdatePayload) -> Company:
        pass

    @abstractmethod
    def delete_by_id(self, id_: Id) -> None:
        pass


class CompanyFounderReadRepository(AbstractReadRepository[CompanyFounder, CompanyFounderFilter], ABC):
    @abstractmethod
    def get_by_id(self, id_: Id) -> CompanyFounder:
        pass

    @abstractmethod
    def get_all(self, filter_: CompanyFounderFilter, pagination: Pagination | None = None) -> list[CompanyFounder]:
        pass


class CompanyFounderWriteRepository(
    AbstractWriteRepository[CompanyFounder, CompanyFounderCreatePayload, CompanyFounderUpdatePayload], ABC
):
    @abstractmethod
    def create(self, data: CompanyFounderCreatePayload) -> CompanyFounder:
        pass

    @abstractmethod
    def update(self, data: CompanyFounderUpdatePayload) -> CompanyFounder:
        pass

    @abstractmethod
    def delete_by_id(self, id_: Id) -> None:
        pass
