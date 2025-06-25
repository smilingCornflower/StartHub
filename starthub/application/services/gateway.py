from application.service_factories.app_service.auth import AuthAppServiceFactory, RegistrationAppServiceFactory
from application.service_factories.app_service.news import NewsAppServiceFactory
from application.service_factories.app_service.project import ProjectAppServiceFactory
from application.service_factories.app_service.user import UserAppServiceFactory
from application.service_factories.app_service.user_favorite import UserFavoriteAppAppServiceFactory
from application.services.auth import AuthAppService, RegistrationAppService
from application.services.news import NewsAppService
from application.services.project import ProjectAppService
from application.services.user import UserAppService
from application.services.user_favorite import UserFavoriteAppService
from infrastructure.services.cookie import CookieService, cookie_service


class Gateway:
    _auth_app_service: AuthAppService | None = None
    _registration_app_service: RegistrationAppService | None = None

    _user_app_service: UserAppService | None = None
    _project_app_service: ProjectAppService | None = None
    _user_favorite_app_service: UserFavoriteAppService | None = None
    _news_app_service: NewsAppService | None = None

    _cookie_service: CookieService | None = None

    @property
    def auth_app_service(self) -> AuthAppService:
        if self._auth_app_service is None:
            self._auth_app_service = AuthAppServiceFactory.create_service()
        return self._auth_app_service

    @property
    def registration_app_service(self) -> RegistrationAppService:
        if self._registration_app_service is None:
            self._registration_app_service = RegistrationAppServiceFactory.create_service()
        return self._registration_app_service

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

    @property
    def news_app_service(self) -> NewsAppService:
        if self._news_app_service is None:
            self._news_app_service = NewsAppServiceFactory.create_service()
        return self._news_app_service

    @property
    def cookie_service(self) -> CookieService:
        if self._cookie_service is None:
            self._cookie_service = cookie_service
        return self._cookie_service


gateway = Gateway()
