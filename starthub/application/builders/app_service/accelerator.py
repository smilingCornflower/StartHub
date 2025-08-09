from application.builders.domain_service.project_management import ProjectAcceleratorServiceBuilder
from application.ports.app_service_builder import AbstractAppServiceBuilder
from application.services.accelerator import AcceleratorAppService
from infrastructure.repositories.project.accelerator import DjProjectAcceleratorReadRepository
from infrastructure.repositories.user import DjUserReadRepository


class AcceleratorAppServiceBuilder(AbstractAppServiceBuilder[AcceleratorAppService]):
    @staticmethod
    def create_service() -> AcceleratorAppService:
        return AcceleratorAppService(
            read_repository=DjProjectAcceleratorReadRepository(),
            user_read_repository=DjUserReadRepository(),
            accelerator_service=ProjectAcceleratorServiceBuilder.create_service(),
        )
