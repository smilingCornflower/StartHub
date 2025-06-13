from application.ports.service_factory import AbstractAppServiceFactory
from application.services.user_favorite import UserFavoriteAppService
from domain.services.user_favorite import UserFavoriteService
from infrastructure.repositories.project_management import DjProjectReadRepository
from infrastructure.repositories.user import DjUserReadRepository
from infrastructure.repositories.user_favorite import DjUserFavoriteReadRepository, DjUserFavoriteWriteRepository


class UserFavoriteAppAppServiceFactory(AbstractAppServiceFactory[UserFavoriteAppService]):
    @staticmethod
    def create_service() -> UserFavoriteAppService:
        return UserFavoriteAppService(
            user_favorite_service=UserFavoriteService(
                user_favorite_read_repository=DjUserFavoriteReadRepository(),
                user_favorite_write_repository=DjUserFavoriteWriteRepository(),
                user_read_repository=DjUserReadRepository(),
                project_read_repository=DjProjectReadRepository(),
            )
        )
