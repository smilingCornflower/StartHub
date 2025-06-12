from application.service_factories.project import ProjectServiceFactory
from application.service_factories.user import UserServiceFactory


class Gateway:
    user_app_service = UserServiceFactory.create_service()
    project_app_service = ProjectServiceFactory.create_service()
