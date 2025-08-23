from application.builders.domain_service.project_management import ProjectServiceBuilder
from application.builders.domain_service.user_management import UserFavoriteServiceBuilder
from application.ports.app_service_builder import AbstractAppServiceBuilder
from application.services.user_management.user_favorite import UserFavoriteAppService
from infrastructure.repositories.project.category import DjProjectCategoryReadRepository
from infrastructure.repositories.project.project import DjProjectReadRepository


class UserFavoriteAppAppServiceBuilder(AbstractAppServiceBuilder[UserFavoriteAppService]):
    @staticmethod
    def create_service() -> UserFavoriteAppService:
        return UserFavoriteAppService(
            user_favorite_service=UserFavoriteServiceBuilder.create_service(),
            project_read_repository=DjProjectReadRepository(),
            project_category_read_repository=DjProjectCategoryReadRepository(),
            project_service=ProjectServiceBuilder.create_service(),
        )
