from application.ports.app_service_factory import AbstractAppServiceFactory
from application.service_factories.domain_service.user_favorite import UserFavoriteServiceFactory
from application.services.user_favorite import UserFavoriteAppService


class UserFavoriteAppAppServiceFactory(AbstractAppServiceFactory[UserFavoriteAppService]):
    @staticmethod
    def create_service() -> UserFavoriteAppService:
        return UserFavoriteAppService(
            user_favorite_service=UserFavoriteServiceFactory.create_service(),
        )
