from domain.models.project_management.accelerator import ProjectAccelerator
from domain.repositories.project.accelerator import ProjectAcceleratorReadRepository, ProjectAcceleratorWriteRepository
from domain.value_objects.common import Pagination
from domain.value_objects.filter import ProjectAcceleratorFilter
from domain.value_objects.project.accelerator import (
    AcceleratorId,
    ProjectAcceleratorCreatePayload,
    ProjectAcceleratorUpdatePayload,
)


class DjProjectAcceleratorReadRepository(ProjectAcceleratorReadRepository):
    def get_by_id(self, id_: AcceleratorId) -> ProjectAccelerator:
        raise NotImplementedError("The method get_by_id() is not implemented yet.")

    def get_all(
        self, filter_: ProjectAcceleratorFilter, pagination: Pagination | None = None
    ) -> list[ProjectAccelerator]:
        raise NotImplementedError("The method get_all() is not implemented yet.")


class DjProjectAcceleratorWriteRepository(ProjectAcceleratorWriteRepository):
    def create(self, data: ProjectAcceleratorCreatePayload) -> ProjectAccelerator:
        raise NotImplementedError("The method create() is not implemented yet.")

    def update(self, data: ProjectAcceleratorUpdatePayload) -> ProjectAccelerator:
        raise NotImplementedError("The method update() is not implemented yet.")

    def delete_by_id(self, id_: AcceleratorId) -> None:
        raise NotImplementedError("The method delete_by_id() is not implemented yet.")
