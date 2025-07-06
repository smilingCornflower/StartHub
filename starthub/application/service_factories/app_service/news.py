from application.ports.app_service_factory import AbstractAppServiceFactory
from application.service_factories.domain_service.news import NewsServiceFactory
from application.service_factories.domain_service.permission import PermissionServiceFactory
from application.service_factories.domain_service.storage import StorageServiceFactory
from application.services.news import NewsAppService
from domain.services.file import ImageService
from domain.services.news import NewsImageService
from infrastructure.repositories.news import DjNewsImageReadRepository, DjNewsImageWriteRepository
from infrastructure.uow import DjangoUnitOfWork


class NewsAppServiceFactory(AbstractAppServiceFactory[NewsAppService]):
    @staticmethod
    def create_service() -> NewsAppService:
        return NewsAppService(
            news_service=NewsServiceFactory.create_service(),
            news_image_service=NewsImageService(
                news_image_read_repository=DjNewsImageReadRepository(),
                news_image_write_repository=DjNewsImageWriteRepository(),
            ),
            permission_service=PermissionServiceFactory.create_service(),
            image_service=ImageService(),
            storage_service=StorageServiceFactory.create_service(),
            unit_of_work=DjangoUnitOfWork(),
        )
