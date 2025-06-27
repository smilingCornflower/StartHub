from abc import ABC, abstractmethod

from domain.models.country import Country
from domain.ports.repository import AbstractReadRepository
from domain.value_objects.common import Id, Pagination
from domain.value_objects.filter import CountryFilter


class CountryReadRepository(AbstractReadRepository[Country, CountryFilter], ABC):
    @abstractmethod
    def get_by_id(self, id_: Id) -> Country:
        """:raises CompanyNotFoundException:"""
        pass

    @abstractmethod
    def get_all(self, filter_: CountryFilter, pagination: Pagination | None = None) -> list[Country]:
        pass
