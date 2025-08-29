from application.builders.domain_service.news import NewsServiceBuilder, NewsTagServiceBuilder
from application.builders.domain_service.permission import PermissionServiceBuilder
from application.ports.app_service_builder import AbstractAppServiceBuilder
from application.services.news_management.news import NewsAppService
from application.services.news_management.news_tag import NewsTagAppService
from domain.services.file import ImageService
from domain.services.news_management.news import NewsImageService
from infrastructure.cloud_storages.google import google_cloud_storage
from infrastructure.repositories.news_management.news import DjNewsReadRepository
from infrastructure.repositories.news_management.news_image import DjNewsImageReadRepository, DjNewsImageWriteRepository
from infrastructure.repositories.user_management.user import DjUserReadRepository
from infrastructure.uow import DjangoUnitOfWork


class NewsAppServiceBuilder(AbstractAppServiceBuilder[NewsAppService]):
    @staticmethod
    def create_service() -> NewsAppService:
        return NewsAppService(
            news_service=NewsServiceBuilder.create_service(),
            news_image_service=NewsImageService(
                news_image_read_repository=DjNewsImageReadRepository(),
                news_image_write_repository=DjNewsImageWriteRepository(),
            ),
            permission_service=PermissionServiceBuilder.create_service(),
            image_service=ImageService(),
            cloud_storage=google_cloud_storage,
            news_read_repository=DjNewsReadRepository(),
            user_read_repository=DjUserReadRepository(),
            unit_of_work=DjangoUnitOfWork(),
        )


class NewsTagAppServiceBuilder(AbstractAppServiceBuilder[NewsTagAppService]):
    @staticmethod
    def create_service() -> NewsTagAppService:
        return NewsTagAppService(
            news_tag_service=NewsTagServiceBuilder.create_service(),
            user_read_repository=DjUserReadRepository(),
            news_read_repository=DjNewsReadRepository(),
        )
