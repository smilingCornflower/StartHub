from application.builders.domain_service.project_management import ProjectStageServiceBuilder
from application.ports.app_service_builder import AbstractAppServiceBuilder
from application.services.project_management.stage import ProjectStageAppService
from infrastructure.repositories.project.stage import DjProjectStageReadRepository
from infrastructure.repositories.user_management.user import DjUserReadRepository


class ProjectStageAppServiceBuilder(AbstractAppServiceBuilder[ProjectStageAppService]):
    @staticmethod
    def create_service() -> ProjectStageAppService:
        return ProjectStageAppService(
            stage_service=ProjectStageServiceBuilder.create_service(),
            user_read_repository=DjUserReadRepository(),
            project_stage_read_reposiotry=DjProjectStageReadRepository(),
        )
