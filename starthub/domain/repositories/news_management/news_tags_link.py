from abc import abstractmethod

from domain.models.news_management.news_tag import NewsTagsLink
from domain.ports.repository import AbstractReadRepository, AbstractWriteRepository
from domain.value_objects.common import Id, Pagination
from domain.value_objects.filter import NewsTagsLinkFilter
from domain.value_objects.news_management.news_tags_link import NewsTagsLinkCreatePayload, NewsTagsLinkUpdatePayload


class NewsTagsLinkReadRepository(AbstractReadRepository[NewsTagsLink, NewsTagsLinkFilter, Id]):
    @abstractmethod
    def get_by_id(self, id_: Id) -> NewsTagsLink:
        pass

    @abstractmethod
    def get_all(self, filter_: NewsTagsLinkFilter, pagination: Pagination | None = None) -> list[NewsTagsLink]:
        pass


class NewsTagsLinkWriteRepository(
    AbstractWriteRepository[NewsTagsLink, NewsTagsLinkCreatePayload, NewsTagsLinkUpdatePayload, Id]
):
    @abstractmethod
    def create(self, data: NewsTagsLinkCreatePayload) -> NewsTagsLink:
        pass

    @abstractmethod
    def update(self, data: NewsTagsLinkUpdatePayload) -> NewsTagsLink:
        pass

    @abstractmethod
    def delete_by_id(self, id_: Id) -> None:
        pass
