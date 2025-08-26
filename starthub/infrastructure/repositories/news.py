from domain.exceptions.news import NewsNotFoundException
from domain.models.news import News, NewsImage
from domain.repositories.news import (
    NewsImageReadRepository,
    NewsImageWriteRepository,
    NewsReadRepository,
    NewsWriteRepository,
)
from domain.value_objects.common import Id, Pagination
from domain.value_objects.filter import NewsFilter, NewsImageFilter
from domain.value_objects.news import (
    NewsCreatePayload,
    NewsImageCreatePayload,
    NewsImageDeletePayload,
    NewsImageUpdatePayload,
    NewsUpdatePayload,
)
from infrastructure.repositories.pagination import apply_pagination


class DjNewsReadRepository(NewsReadRepository):
    def get_by_id(self, id_: Id) -> News:
        """:raises NewsNotFoundException:"""
        news: News | None = News.objects.filter(id=id_.value).first()
        if news is None:
            raise NewsNotFoundException(f"News with id = {id_.value} not found.")
        return news

    def get_all(self, filter_: NewsFilter, pagination: Pagination | None = None) -> list[News]:
        qs = News.objects.all()

        # Order By
        if filter_.order_by_lst:
            for order_by in filter_.order_by_lst:
                qs = qs.order_by(order_by)

        if filter_.published_at_start:
            qs = qs.filter(published_at__gte=filter_.published_at_start)
        if filter_.published_at_end:
            qs = qs.filter(published_at__lte=filter_.published_at_end)

        if pagination:
            return apply_pagination(qs, pagination=pagination)

        return list(qs)


class DjNewsWriteRepository(NewsWriteRepository):
    def create(self, data: NewsCreatePayload) -> News:
        return News.objects.create(
            title=data.title.value,
            subtitle=data.subtitle.value if data.subtitle else None,
            content=data.content.value,
            author_id=data.author_id.value,
        )

    def update(self, data: NewsUpdatePayload) -> News:
        """:raises NewsNotFoundException:"""
        news: News | None = News.objects.filter(id=data.news_id.value).first()
        if news is None:
            raise NewsNotFoundException(f"News with id = {data.news_id.value} not found.")

        if data.title is not None:
            news.title = data.title.value
        if data.subtitle is not None:
            news.subtitle = data.subtitle.value
        if data.content is not None:
            news.content = data.content.value
        if data.cover_path is not None:
            news.cover = data.cover_path
        if data.is_active is not None:
            news.is_active = data.is_active

        news.save()
        return news

    def delete_by_id(self, id_: Id) -> None:
        News.objects.filter(id=id_.value).delete()


class DjNewsImageReadRepository(NewsImageReadRepository):
    def get_by_id(self, id_: Id) -> NewsImage:
        raise NotImplementedError("The method get_by_id() is not implemented yet.")

    def get_all(self, filter_: NewsImageFilter, pagination: Pagination | None = None) -> list[NewsImage]:
        qs = NewsImage.objects.all()

        if filter_.news_id is not None:
            qs = qs.filter(news_id=filter_.news_id.value)

        return list(qs)


class DjNewsImageWriteRepository(NewsImageWriteRepository):
    def create(self, data: NewsImageCreatePayload) -> NewsImage:
        return NewsImage.objects.create(news_id=data.news_id.value, image=data.image)

    def update(self, data: NewsImageUpdatePayload) -> NewsImage:
        raise NotImplementedError("The method update() is not implemented yet.")

    def delete_by_id(self, id_: Id) -> None:
        pass

    def delete(self, data: NewsImageDeletePayload) -> None:
        try:
            news_image = NewsImage.objects.get(image=data.file_name)
            news_image.delete()
        except NewsImage.DoesNotExist:
            pass
