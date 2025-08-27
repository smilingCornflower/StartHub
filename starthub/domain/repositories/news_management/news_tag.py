from abc import ABC, abstractmethod

from domain.models.news_management.news_tag import NewsTag
from domain.ports.repository import AbstractReadRepository, AbstractWriteRepository
from domain.value_objects.common import Pagination
from domain.value_objects.filter import NewsTagFilter
from domain.value_objects.news_management.news_tag import NewsTagCreatePayload, NewsTagId, NewsTagUpdatePayload


class NewsTagReadRepository(AbstractReadRepository[NewsTag, NewsTagFilter, NewsTagId], ABC):
    @abstractmethod
    def get_by_id(self, id_: NewsTagId) -> NewsTag:
        pass

    @abstractmethod
    def get_all(self, filter_: NewsTagFilter, pagination: Pagination | None = None) -> list[NewsTag]:
        pass


class NewsTagWriteRepository(
    AbstractWriteRepository[NewsTag, NewsTagCreatePayload, NewsTagUpdatePayload, NewsTagId], ABC
):
    @abstractmethod
    def create(self, data: NewsTagCreatePayload) -> NewsTag:
        pass

    @abstractmethod
    def update(self, data: NewsTagUpdatePayload) -> NewsTag:
        pass

    @abstractmethod
    def delete_by_id(self, id_: NewsTagId) -> None:
        pass
