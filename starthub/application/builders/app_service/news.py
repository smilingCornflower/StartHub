from application.builders.domain_service.news import NewsServiceBuilder
from application.builders.domain_service.permission import PermissionServiceBuilder
from application.builders.domain_service.storage import StorageServiceBuilder
from application.ports.app_service_builder import AbstractAppServiceBuilder
from application.services.news import NewsAppService
from domain.services.file import ImageService
from domain.services.news import NewsImageService
from infrastructure.repositories.news import DjNewsImageReadRepository, DjNewsImageWriteRepository
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
            storage_service=StorageServiceBuilder.create_service(),
            unit_of_work=DjangoUnitOfWork(),
        )
