from domain.models.project_management.incubator import ProjectIncubator
from domain.repositories.project.incubator import PojectIncubatorReadRepository, ProjectIncubatorWriteRepository
from domain.value_objects.common import Pagination
from domain.value_objects.filter import ProjectIncubatorFilter
from domain.value_objects.project.incubator import IncubatorCreatePayload, IncubatorId, IncubatorUpdatePayload


class DjProjectIncubatorReadRepository(PojectIncubatorReadRepository):
    def get_by_id(self, id_: IncubatorId) -> ProjectIncubator:
        raise NotImplementedError("The method get_by_id() is not implemented yet.")

    def get_all(self, filter_: ProjectIncubatorFilter, pagination: Pagination | None = None) -> list[ProjectIncubator]:
        raise NotImplementedError("The method get_all() is not implemented yet.")


class DjProjectIncubatorWriteRepository(ProjectIncubatorWriteRepository):
    def create(self, data: IncubatorCreatePayload) -> ProjectIncubator:
        return ProjectIncubator.objects.create(
            project_id=data.project_id.value,
            name=data.name.value,
            description=data.description.value,
        )

    def update(self, data: IncubatorUpdatePayload) -> ProjectIncubator:
        raise NotImplementedError("The method update() is not implemented yet.")

    def delete_by_id(self, id_: IncubatorId) -> None:
        raise NotImplementedError("The method delete_by_id() is not implemented yet.")
