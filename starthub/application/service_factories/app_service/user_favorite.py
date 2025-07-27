from application.ports.app_service_factory import AbstractAppServiceFactory
from application.service_factories.domain_service.project_management import ProjectServiceBuilder
from application.service_factories.domain_service.user_favorite import UserFavoriteServiceBuilder
from application.services.user_favorite import UserFavoriteAppService
from infrastructure.repositories.project_management import DjProjectReadRepository


class UserFavoriteAppAppServiceFactory(AbstractAppServiceFactory[UserFavoriteAppService]):
    @staticmethod
    def create_service() -> UserFavoriteAppService:
        return UserFavoriteAppService(
            user_favorite_service=UserFavoriteServiceBuilder.create_service(),
            project_read_repository=DjProjectReadRepository(),
            project_service=ProjectServiceBuilder.create_service(),
        )
