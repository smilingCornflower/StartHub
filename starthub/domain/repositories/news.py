from abc import ABC, abstractmethod

from domain.models.news import News
from domain.ports.repository import AbstractReadRepository, AbstractWriteRepository
from domain.value_objects.common import Id, Pagination
from domain.value_objects.filter import NewsFilter
from domain.value_objects.news import NewsCreatePayload, NewsUpdatePayload


# noinspection DuplicatedCode
class NewsReadRepository(AbstractReadRepository[News, NewsFilter], ABC):
    @abstractmethod
    def get_by_id(self, id_: Id) -> News:
        pass

    @abstractmethod
    def get_all(self, filter_: NewsFilter, pagination: Pagination | None = None) -> list[News]:
        pass


class NewsWriteRepository(AbstractWriteRepository[News, NewsCreatePayload, NewsUpdatePayload], ABC):
    @abstractmethod
    def create(self, data: NewsCreatePayload) -> News:
        pass

    @abstractmethod
    def update(self, data: NewsUpdatePayload) -> News:
        pass

    @abstractmethod
    def delete_by_id(self, id_: Id) -> None:
        pass
