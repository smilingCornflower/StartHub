from domain.models.news import News
from domain.repositories.news import NewsReadRepository, NewsWriteRepository
from domain.value_objects.common import Id
from domain.value_objects.filter import NewsFilter
from domain.value_objects.news import NewsCreatePayload, NewsUpdatePayload


class DjNewsReadRepository(NewsReadRepository):
    def get_by_id(self, id_: Id) -> News:
        raise NotImplementedError("The method get_by_id() not implemented yet.")

    def get_all(self, filter_: NewsFilter) -> list[News]:
        raise NotImplementedError("The method get_all() not implemented yet.")


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
