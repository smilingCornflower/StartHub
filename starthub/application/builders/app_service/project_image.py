from application.builders.domain_service.project_management import ProjectImageServiceBuilder
from application.ports.app_service_builder import AbstractAppServiceBuilder
from application.services.project_image import ProjectImageAppService


class ProjectImageAppServiceBuilder(AbstractAppServiceBuilder[ProjectImageAppService]):
    @staticmethod
    def create_service() -> ProjectImageAppService:
        return ProjectImageAppService(
            project_image_service=ProjectImageServiceBuilder.create_service(),
        )
