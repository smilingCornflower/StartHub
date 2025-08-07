from domain.ports.service import AbstractDomainService
from domain.repositories.project.incubator import ProjectIncubatorWriteRepository
from domain.value_objects.project.incubator import IncubatorCreatePayload, IncubatorUpdatePayload


class IncubatorService(AbstractDomainService):
    def __init__(
        self,
        write_repository: ProjectIncubatorWriteRepository,
    ):
        self._write_repository = write_repository

    def create(self, payload: IncubatorCreatePayload) -> None:
        self._write_repository.create(data=payload)

    def update(self, payload: IncubatorUpdatePayload) -> None:
        self._write_repository.update(data=payload)
