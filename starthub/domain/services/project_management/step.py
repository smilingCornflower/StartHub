from domain.models.project_management.step import ProjectStep
from domain.ports.service import AbstractDomainService
from domain.repositories.project.step import ProjectStepWriteRepository
from domain.value_objects.project.step import ProjectStepCreatePaylaod


class ProjectStepService(AbstractDomainService):
    def __init__(
        self,
        write_repository: ProjectStepWriteRepository,
    ):
        self._write_repository = write_repository

    def create(self, paylaod: ProjectStepCreatePaylaod) -> ProjectStep:
        project_step: ProjectStep = self._write_repository.create(data=paylaod)
        return project_step
