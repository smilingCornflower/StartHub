from domain.models.project import Project
from domain.repositories.project import ProjectReadRepository, ProjectWriteRepository
from domain.value_objects.project import ProjectCreatePayload


class ProjectService:
    def __init__(self, read_repository: ProjectReadRepository, write_repository: ProjectWriteRepository):
        self._read_repository = read_repository
        self._write_repository = write_repository

    def create(self, create_payload: ProjectCreatePayload) -> Project:
        return self._write_repository.create(create_payload)
