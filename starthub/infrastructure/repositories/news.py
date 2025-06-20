from domain.exceptions.news import NewsNotFoundException
from domain.models.news import News
from domain.repositories.news import NewsReadRepository, NewsWriteRepository
from domain.value_objects.common import Id
from domain.value_objects.filter import NewsFilter
from domain.value_objects.news import NewsCreatePayload, NewsUpdatePayload


class DjNewsReadRepository(NewsReadRepository):
    def get_by_id(self, id_: Id) -> News:
        news: News | None = News.objects.filter(id=id_.value).first()
        if news is None:
            raise NewsNotFoundException(f"News with id = {id_.value} not found.")
        return news

    def get_all(self, filter_: NewsFilter) -> list[News]:
        qs = News.objects.all().order_by("-id")
        if filter_.last_id is not None:
            qs = qs.filter(id__lt=filter_.last_id)
        return list(qs[:filter_.limit])


class DjNewsWriteRepository(NewsWriteRepository):
    def create(self, data: NewsCreatePayload) -> News:
        return News.objects.create(
            title=data.title.value,
            content=data.content.value,
            author_id=data.author_id.value,
            image=data.image_url,
        )

    def update(self, data: NewsUpdatePayload) -> News:
        raise NotImplementedError("The method update() not implemented yet.")

    def delete_by_id(self, id_: Id) -> None:
        raise NotImplementedError("The method delete_by_id() not implemented yet.")
