from application.ports.domain_service_factory import AbstractDomainServiceFactory
from domain.services.file import ImageService
from domain.services.news import NewsService
from infrastructure.cloud_storages.google import google_cloud_storage
from infrastructure.repositories.news import DjNewsReadRepository, DjNewsWriteRepository


class NewsServiceFactory(AbstractDomainServiceFactory[NewsService]):
    @staticmethod
    def create_service() -> NewsService:
        return NewsService(
            news_read_repository=DjNewsReadRepository(),
            news_write_repository=DjNewsWriteRepository(),
            cloud_storage=google_cloud_storage,
            image_service=ImageService(),
        )
