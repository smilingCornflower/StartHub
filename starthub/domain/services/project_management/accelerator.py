from domain.models.project_management.accelerator import ProjectAccelerator
from domain.ports.service import AbstractDomainService
from domain.repositories.project.accelerator import ProjectAcceleratorWriteRepository
from domain.value_objects.project.accelerator import ProjectAcceleratorCreatePayload, ProjectAcceleratorUpdatePayload


class ProjectAcceleratorService(AbstractDomainService):
    def __init__(
        self,
        write_repository: ProjectAcceleratorWriteRepository,
    ):
        self._write_repository = write_repository

    def create(self, payload: ProjectAcceleratorCreatePayload) -> ProjectAccelerator:
        return self._write_repository.create(data=payload)

    def update(self, payload: ProjectAcceleratorUpdatePayload) -> ProjectAccelerator:
        return self._write_repository.update(data=payload)
