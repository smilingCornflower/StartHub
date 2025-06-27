from domain.exceptions.news import NewsNotFoundException
from domain.models.news import News
from domain.repositories.news import NewsReadRepository, NewsWriteRepository
from domain.value_objects.common import Id, Pagination
from domain.value_objects.filter import NewsFilter
from domain.value_objects.news import NewsCreatePayload, NewsUpdatePayload


class DjNewsReadRepository(NewsReadRepository):
    def get_by_id(self, id_: Id) -> News:
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
            content=data.content.value,
            author_id=data.author_id.value,
            image=data.image_url,
        )

    def update(self, data: NewsUpdatePayload) -> News:
        """:raises NewsNotFoundException:"""
        news: News | None = News.objects.filter(id=data.news_id.value).first()
        if news is None:
            raise NewsNotFoundException(f"News with id = {data.news_id.value} not found.")

        if data.title:
            news.title = data.title.value
        if data.content:
            news.content = data.content.value
        if data.image_url:
            news.image = data.image_url

        news.save()
        return news

    def delete_by_id(self, id_: Id) -> None:
        News.objects.filter(id=id_.value).delete()
