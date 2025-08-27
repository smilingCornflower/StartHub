from abc import ABC, abstractmethod

from domain.models.news_management.news_image import NewsImage
from domain.ports.repository import AbstractReadRepository, AbstractWriteRepository
from domain.value_objects.common import CursorPagination, Id, OffsetPagination
from domain.value_objects.filter import NewsImageFilter
from domain.value_objects.news_management.news_image import (
    NewsImageCreatePayload,
    NewsImageDeletePayload,
    NewsImageUpdatePayload,
)


class NewsImageReadRepository(AbstractReadRepository[NewsImage, NewsImageFilter, Id], ABC):
    @abstractmethod
    def get_by_id(self, id_: Id) -> NewsImage:
        pass

    @abstractmethod
    def get_all(
        self, filter_: NewsImageFilter, pagination: CursorPagination | OffsetPagination | None = None
    ) -> list[NewsImage]:
        pass


class NewsImageWriteRepository(
    AbstractWriteRepository[NewsImage, NewsImageCreatePayload, NewsImageUpdatePayload, Id], ABC
):
    @abstractmethod
    def create(self, data: NewsImageCreatePayload) -> NewsImage:
        pass

    @abstractmethod
    def update(self, data: NewsImageUpdatePayload) -> NewsImage:
        pass

    @abstractmethod
    def delete_by_id(self, id_: Id) -> None:
        pass

    @abstractmethod
    def delete(self, data: NewsImageDeletePayload) -> None:
        pass
