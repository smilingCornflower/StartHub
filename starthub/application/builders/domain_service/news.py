from application.ports.domain_service_builder import AbstractDomainServiceBuilder
from domain.services.news import NewsImageService, NewsService
from infrastructure.repositories.news import (
    DjNewsImageReadRepository,
    DjNewsImageWriteRepository,
    DjNewsReadRepository,
    DjNewsWriteRepository,
)


class NewsServiceBuilder(AbstractDomainServiceBuilder[NewsService]):
    @staticmethod
    def create_service() -> NewsService:
        return NewsService(
            news_read_repository=DjNewsReadRepository(),
            news_write_repository=DjNewsWriteRepository(),
        )


class NewsImageServiceBuilder(AbstractDomainServiceBuilder[NewsImageService]):
    @staticmethod
    def create_service() -> NewsImageService:
        return NewsImageService(
            news_image_read_repository=DjNewsImageReadRepository(),
            news_image_write_repository=DjNewsImageWriteRepository(),
        )
