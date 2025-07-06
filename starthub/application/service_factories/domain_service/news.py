from application.ports.domain_service_factory import AbstractDomainServiceFactory
from domain.services.news import NewsImageService, NewsService
from infrastructure.repositories.news import (
    DjNewsImageReadRepository,
    DjNewsImageWriteRepository,
    DjNewsReadRepository,
    DjNewsWriteRepository,
)


class NewsServiceFactory(AbstractDomainServiceFactory[NewsService]):
    @staticmethod
    def create_service() -> NewsService:
        return NewsService(
            news_read_repository=DjNewsReadRepository(),
            news_write_repository=DjNewsWriteRepository(),
        )


class NewsImageServiceFactory(AbstractDomainServiceFactory[NewsImageService]):
    @staticmethod
    def create_service() -> NewsImageService:
        return NewsImageService(
            news_image_read_repository=DjNewsImageReadRepository(),
            news_image_write_repository=DjNewsImageWriteRepository(),
        )
