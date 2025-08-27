from domain.models.news_management.news_tag import NewsTagsLink
from domain.repositories.news_management.news_tags_link import NewsTagsLinkReadRepository, NewsTagsLinkWriteRepository
from domain.value_objects.common import Id, Pagination
from domain.value_objects.filter import NewsTagsLinkFilter
from domain.value_objects.news_management.news_tags_link import NewsTagsLinkCreatePayload, NewsTagsLinkUpdatePayload


class DjNewsTagsLinkReadRepository(NewsTagsLinkReadRepository):
    def get_by_id(self, id_: Id) -> NewsTagsLink:
        raise NotImplementedError("The method get_by_id() is not implemented.")

    def get_all(self, filter_: NewsTagsLinkFilter, pagination: Pagination | None = None) -> list[NewsTagsLink]:
        raise NotImplementedError("The method get_all() is not implemented.")


class DjNewsTagsLinkWriteRepository(NewsTagsLinkWriteRepository):
    def create(self, data: NewsTagsLinkCreatePayload) -> NewsTagsLink:
        return NewsTagsLink.objects.create(news_id=data.news_id.value, tag_id=data.news_tag_id.value)

    def update(self, data: NewsTagsLinkUpdatePayload) -> NewsTagsLink:
        raise NotImplementedError("The method update() is not implemented.")

    def delete_by_id(self, id_: Id) -> None:
        raise NotImplementedError("The method delete_by_id() is not implemented.")
