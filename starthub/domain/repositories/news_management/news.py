from abc import ABC, abstractmethod

from domain.models.news_management.news import News
from domain.ports.repository import AbstractReadRepository, AbstractWriteRepository
from domain.value_objects.common import Id, Pagination
from domain.value_objects.filter import NewsFilter
from domain.value_objects.news_management.news import NewsCreatePayload, NewsUpdatePayload


class NewsReadRepository(AbstractReadRepository[News, NewsFilter, Id], ABC):
    @abstractmethod
    def get_by_id(self, id_: Id) -> News:
        """:raises NewsNotFoundException:"""
        pass

    @abstractmethod
    def get_all(self, filter_: NewsFilter, pagination: Pagination | None = None) -> list[News]:
        pass


class NewsWriteRepository(AbstractWriteRepository[News, NewsCreatePayload, NewsUpdatePayload, Id], ABC):
    @abstractmethod
    def create(self, data: NewsCreatePayload) -> News:
        pass

    @abstractmethod
    def update(self, data: NewsUpdatePayload) -> News:
        pass

    @abstractmethod
    def delete_by_id(self, id_: Id) -> None:
        pass
