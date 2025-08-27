from application.builders.domain_service.permission import PermissionServiceBuilder
from application.ports.domain_service_builder import AbstractDomainServiceBuilder
from domain.services.news_management.news import NewsImageService, NewsService
from domain.services.news_management.news_tag import NewsTagService
from infrastructure.repositories.news_management.news import DjNewsReadRepository, DjNewsWriteRepository
from infrastructure.repositories.news_management.news_image import DjNewsImageReadRepository, DjNewsImageWriteRepository
from infrastructure.repositories.news_management.news_tag import DjNewsTagReadRepository
from infrastructure.repositories.news_management.news_tags_link import DjNewsTagsLinkWriteRepository


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


class NewsTagServiceBuilder(AbstractDomainServiceBuilder[NewsTagService]):
    @staticmethod
    def create_service() -> NewsTagService:
        return NewsTagService(
            permission_service=PermissionServiceBuilder.create_service(),
            news_tag_read_repository=DjNewsTagReadRepository(),
            news_tags_link_write_repository=DjNewsTagsLinkWriteRepository(),
        )
