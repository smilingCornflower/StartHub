from application.ports.domain_service_factory import AbstractDomainServiceFactory
from domain.services.user_management import UserFavoriteService
from infrastructure.repositories.project_management import DjProjectReadRepository
from infrastructure.repositories.user import DjUserReadRepository
from infrastructure.repositories.user_favorite import DjUserFavoriteReadRepository, DjUserFavoriteWriteRepository


class UserFavoriteServiceFactory(AbstractDomainServiceFactory[UserFavoriteService]):
    @staticmethod
    def create_service() -> UserFavoriteService:
        return UserFavoriteService(
            user_favorite_read_repository=DjUserFavoriteReadRepository(),
            user_favorite_write_repository=DjUserFavoriteWriteRepository(),
            user_read_repository=DjUserReadRepository(),
            project_read_repository=DjProjectReadRepository(),
        )
