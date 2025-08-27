from domain.exceptions.news import NewsTagNotFoundException
from domain.models.news_management.news_tag import NewsTag
from domain.repositories.news_management.news_tag import NewsTagReadRepository, NewsTagWriteRepository
from domain.value_objects.common import Pagination
from domain.value_objects.filter import NewsTagFilter
from domain.value_objects.news_management.news_tag import NewsTagCreatePayload, NewsTagId, NewsTagUpdatePayload
from infrastructure.repositories.pagination import apply_pagination


class DjNewsTagReadRepository(NewsTagReadRepository):
    def get_by_id(self, id_: NewsTagId) -> NewsTag:
        """:raises NewsTagNotFoundException:"""
        tag = NewsTag.objects.filter(id=id_.value).first()
        if tag is None:
            raise NewsTagNotFoundException(f"News tag with id = {id_.value} not found.")
        return tag

    def get_all(self, filter_: NewsTagFilter, pagination: Pagination | None = None) -> list[NewsTag]:
        qs = NewsTag.objects.all()

        if filter_.tag_names:
            qs = qs.filter(name__in=filter_.tag_names)

        if pagination:
            return apply_pagination(qs, pagination=pagination)

        return list(qs)


class DjNewsTagWriteRepository(NewsTagWriteRepository):
    def create(self, data: NewsTagCreatePayload) -> NewsTag:
        return NewsTag.objects.create(name=data.name)

    def update(self, data: NewsTagUpdatePayload) -> NewsTag:
        raise NotImplementedError("The method update() is not implemented.")

    def delete_by_id(self, id_: NewsTagId) -> None:
        raise NotImplementedError("The method delete_by_id() is not implemented.")
