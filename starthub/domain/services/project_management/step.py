from domain.ports.service import AbstractDomainService
from domain.repositories.project.step import ProjectStepWriteRepository
from domain.value_objects.project.step import ProjectStepCreatePaylaod


class ProjectStepService(AbstractDomainService):
    def __init__(
        self,
        write_repository: ProjectStepWriteRepository,
    ):
        self._write_repository = write_repository

    def create(self, paylaod: ProjectStepCreatePaylaod) -> None:
        self._write_repository.create(data=paylaod)
