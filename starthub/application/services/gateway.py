from application.service_factories.project import ProjectServiceFactory
from application.service_factories.user import UserServiceFactory
from application.services.project import ProjectAppService
from application.services.user import UserAppService


class Gateway:
    _user_app_service: UserAppService | None = None
    _project_app_service: ProjectAppService | None = None

    @property
    def user_app_service(self) -> UserAppService:
        if self._user_app_service is None:
            self._user_app_service = UserServiceFactory.create_service()
        return self._user_app_service

    @property
    def project_app_service(self) -> ProjectAppService:
        if self._project_app_service is None:
            self._project_app_service = ProjectServiceFactory.create_service()
        return self._project_app_service


gateway = Gateway()
