from domain.models.news_management.news_image import NewsImage
from domain.repositories.news_management.news_image import NewsImageReadRepository, NewsImageWriteRepository
from domain.value_objects.common import Id, Pagination
from domain.value_objects.filter import NewsImageFilter
from domain.value_objects.news_management.news_image import (
    NewsImageCreatePayload,
    NewsImageDeletePayload,
    NewsImageUpdatePayload,
)


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
