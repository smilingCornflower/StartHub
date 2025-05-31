from abc import ABC, abstractmethod

from domain.models.company import Company
from domain.ports.repository import AbstractReadRepository, AbstractWriteRepository
from domain.value_objects.common import Id
from domain.value_objects.company import CompanyCreatePayload, CompanyUpdatePayload
from domain.value_objects.filter import CompanyFilter


class CompanyReadRepository(AbstractReadRepository[Company, CompanyFilter], ABC):
    @abstractmethod
    def get_by_id(self, id_: Id) -> Company:
        pass

    @abstractmethod
    def get_all(self, filter_: CompanyFilter) -> list[Company]:
        pass


class CompanyWriteRepository(AbstractWriteRepository[Company, CompanyCreatePayload, CompanyUpdatePayload], ABC):
    @abstractmethod
    def create(self, data: CompanyCreatePayload) -> Company:
        pass

    @abstractmethod
    def update(self, data: CompanyUpdatePayload) -> Company:
        pass

    @abstractmethod
    def delete(self, id_: Id) -> None:
        pass
