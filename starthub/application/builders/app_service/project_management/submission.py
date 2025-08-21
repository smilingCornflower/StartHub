from application.builders.domain_service.project_management import ProjectSubmissionServiceBuilder
from application.ports.app_service_builder import AbstractAppServiceBuilder
from application.services.project_management.submission import ProjectSubmissionAppService
from infrastructure.repositories.project.project import DjProjectReadRepository
from infrastructure.repositories.user import DjUserReadRepository


class ProjectSubmissionAppServiceBuilder(AbstractAppServiceBuilder[ProjectSubmissionAppService]):
    @staticmethod
    def create_service() -> ProjectSubmissionAppService:
        return ProjectSubmissionAppService(
            project_submission_service=ProjectSubmissionServiceBuilder.create_service(),
            user_read_repository=DjUserReadRepository(),
            project_read_repository=DjProjectReadRepository(),
        )
