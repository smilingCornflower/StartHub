from application.service_factories.project import ProjectAppServiceFactory
from application.service_factories.user import UserAppServiceFactory
from application.service_factories.user_favorite import UserFavoriteAppAppServiceFactory
from application.services.project import ProjectAppService
from application.services.user import UserAppService
from application.services.user_favorite import UserFavoriteAppService


class Gateway:
    _user_app_service: UserAppService | None = None
    _project_app_service: ProjectAppService | None = None
    _user_favorite_app_service: UserFavoriteAppService | None = None

    @property
    def user_app_service(self) -> UserAppService:
        if self._user_app_service is None:
            self._user_app_service = UserAppServiceFactory.create_service()
        return self._user_app_service

    @property
    def project_app_service(self) -> ProjectAppService:
        if self._project_app_service is None:
            self._project_app_service = ProjectAppServiceFactory.create_service()
        return self._project_app_service

    @property
    def user_favorite_app_service(self) -> UserFavoriteAppService:
        if self._user_favorite_app_service is None:
            self._user_favorite_app_service = UserFavoriteAppAppServiceFactory.create_service()
        return self._user_favorite_app_service


gateway = Gateway()
