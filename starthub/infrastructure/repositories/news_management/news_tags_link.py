from domain.exceptions.news import NewsTagNotFoundException
from domain.models.news_management.news_tag import NewsTagsLink
from domain.repositories.news_management.news_tags_link import NewsTagsLinkReadRepository, NewsTagsLinkWriteRepository
from domain.value_objects.common import CursorPagination, Id, OffsetPagination
from domain.value_objects.filter import NewsTagsLinkFilter
from domain.value_objects.news_management.news_tags_link import NewsTagsLinkCreatePayload, NewsTagsLinkUpdatePayload
from loguru import logger


class DjNewsTagsLinkReadRepository(NewsTagsLinkReadRepository):
    def get_by_id(self, id_: Id) -> NewsTagsLink:
        raise NotImplementedError("The method get_by_id() is not implemented.")

    def get_all(
        self, filter_: NewsTagsLinkFilter, pagination: CursorPagination | OffsetPagination | None = None
    ) -> list[NewsTagsLink]:
        raise NotImplementedError("The method get_all() is not implemented.")


class DjNewsTagsLinkWriteRepository(NewsTagsLinkWriteRepository):
    def delete_by_association_ids(self, news_id: Id, tag_id: Id) -> None:
        """:raises NewsTagNotFoundException:"""
        try:
            NewsTagsLink.objects.get(news_id=news_id.value, tag_id=tag_id.value).delete()
        except NewsTagsLink.DoesNotExist:
            logger.error(f"NewsTagLink not found by association_ids = ({news_id.value}, {tag_id.value})")
            raise NewsTagNotFoundException(
                f"There is no tag with id = {tag_id.value} for the news with id = {news_id.value}."
            )

    def get_or_create(self, data: NewsTagsLinkCreatePayload) -> tuple[NewsTagsLink, bool]:
        return NewsTagsLink.objects.get_or_create(news_id=data.news_id.value, tag_id=data.news_tag_id.value)

    def create(self, data: NewsTagsLinkCreatePayload) -> NewsTagsLink:
        return NewsTagsLink.objects.create(news_id=data.news_id.value, tag_id=data.news_tag_id.value)

    def update(self, data: NewsTagsLinkUpdatePayload) -> NewsTagsLink:
        raise NotImplementedError("The method update() is not implemented.")

    def delete_by_id(self, id_: Id) -> None:
        raise NotImplementedError("The method delete_by_id() is not implemented.")
