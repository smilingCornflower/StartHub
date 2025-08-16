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


class DjNewsReadRepository(NewsReadRepository):
    def get_by_id(self, id_: Id) -> News:
        """:raises NewsNotFoundException:"""
        news: News | None = News.objects.filter(id=id_.value).first()
        if news is None:
            raise NewsNotFoundException(f"News with id = {id_.value} not found.")
        return news

    def get_all(self, filter_: NewsFilter, pagination: Pagination | None = None) -> list[News]:
        qs = News.objects.all().order_by("-id")

        if pagination and pagination.last_id is not None:
            qs = qs.filter(id__lt=pagination.last_id)
        if pagination:
            qs = qs[: pagination.limit]
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

        if data.title:
            news.title = data.title.value
        if data.subtitle:
            news.subtitle = data.subtitle.value
        if data.content:
            news.content = data.content.value
        if data.cover_path:
            news.cover = data.cover_path

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
