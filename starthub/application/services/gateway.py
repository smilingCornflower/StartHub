from application.builders.app_service.auth import AuthAppServiceBuilder, RegistrationAppServiceBuilder
from application.builders.app_service.news import NewsAppServiceBuilder
from application.builders.app_service.project import (
    ProjectCreateAppServiceBuilder,
    ProjectDeleteAppServiceBuilder,
    ProjectGetAppServiceBuilder,
    ProjectUpdateAppServiceBuilder,
)
from application.builders.app_service.project_image import ProjectImageAppServiceBuilder
from application.builders.app_service.user import UserAppServiceBuilder
from application.builders.app_service.user_favorite import UserFavoriteAppAppServiceBuilder
from application.services.auth import AuthAppService, RegistrationAppService
from application.services.news import NewsAppService
from application.services.project import (
    ProjectCreateAppService,
    ProjectDeleteAppService,
    ProjectGetAppService,
    ProjectUpdateAppService,
)
from application.services.project_image import ProjectImageAppService
from application.services.user import UserAppService
from application.services.user_favorite import UserFavoriteAppService
from infrastructure.services.cookie import CookieService, cookie_service


class Gateway:
    _auth_app_service: AuthAppService | None = None
    _registration_app_service: RegistrationAppService | None = None

    _user_app_service: UserAppService | None = None

    _project_create_app_service: ProjectCreateAppService | None = None
    _project_update_app_service: ProjectUpdateAppService | None = None
    _project_get_app_service: ProjectGetAppService | None = None
    _project_delete_app_service: ProjectDeleteAppService | None = None

    _project_image_app_service: ProjectImageAppService | None = None
    _user_favorite_app_service: UserFavoriteAppService | None = None
    _news_app_service: NewsAppService | None = None

    _cookie_service: CookieService | None = None

    @property
    def auth_app_service(self) -> AuthAppService:
        if self._auth_app_service is None:
            self._auth_app_service = AuthAppServiceBuilder.create_service()
        return self._auth_app_service

    @property
    def registration_app_service(self) -> RegistrationAppService:
        if self._registration_app_service is None:
            self._registration_app_service = RegistrationAppServiceBuilder.create_service()
        return self._registration_app_service

    @property
    def user_app_service(self) -> UserAppService:
        if self._user_app_service is None:
            self._user_app_service = UserAppServiceBuilder.create_service()
        return self._user_app_service

    @property
    def project_create_app_service(self) -> ProjectCreateAppService:
        if self._project_create_app_service is None:
            self._project_create_app_service = ProjectCreateAppServiceBuilder.create_service()
        return self._project_create_app_service

    @property
    def project_update_app_service(self) -> ProjectUpdateAppService:
        if self._project_update_app_service is None:
            self._project_update_app_service = ProjectUpdateAppServiceBuilder.create_service()
        return self._project_update_app_service

    @property
    def project_get_app_service(self) -> ProjectGetAppService:
        if self._project_get_app_service is None:
            self._project_get_app_service = ProjectGetAppServiceBuilder.create_service()
        return self._project_get_app_service

    @property
    def project_delete_app_service(self) -> ProjectDeleteAppService:
        if self._project_delete_app_service is None:
            self._project_delete_app_service = ProjectDeleteAppServiceBuilder.create_service()
        return self._project_delete_app_service

    @property
    def project_image_app_service(self) -> ProjectImageAppService:
        if self._project_image_app_service is None:
            self._project_image_app_service = ProjectImageAppServiceBuilder.create_service()
        return self._project_image_app_service

    @property
    def user_favorite_app_service(self) -> UserFavoriteAppService:
        if self._user_favorite_app_service is None:
            self._user_favorite_app_service = UserFavoriteAppAppServiceBuilder.create_service()
        return self._user_favorite_app_service

    @property
    def news_app_service(self) -> NewsAppService:
        if self._news_app_service is None:
            self._news_app_service = NewsAppServiceBuilder.create_service()
        return self._news_app_service

    @property
    def cookie_service(self) -> CookieService:
        if self._cookie_service is None:
            self._cookie_service = cookie_service
        return self._cookie_service


gateway = Gateway()
