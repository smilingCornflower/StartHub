from domain.exceptions.project_management import ProjectIncubatorNotFoundException
from domain.models.project_management.incubator import ProjectIncubator
from domain.repositories.project.incubator import PojectIncubatorReadRepository, ProjectIncubatorWriteRepository
from domain.value_objects.common import Pagination
from domain.value_objects.filter import ProjectIncubatorFilter
from domain.value_objects.project.incubator import IncubatorCreatePayload, IncubatorId, IncubatorUpdatePayload
from infrastructure.repositories.pagination import apply_pagination


class DjProjectIncubatorReadRepository(PojectIncubatorReadRepository):
    def get_by_id(self, id_: IncubatorId) -> ProjectIncubator:
        raise NotImplementedError("The method get_by_id() is not implemented yet.")

    def get_all(self, filter_: ProjectIncubatorFilter, pagination: Pagination | None = None) -> list[ProjectIncubator]:
        queryset = ProjectIncubator.objects.all()
        if filter_.project_id is not None:
            queryset = queryset.filter(project_id=filter_.project_id.value)

        if pagination is not None:
            return apply_pagination(queryset=queryset, pagination=pagination)
        return list(queryset)


class DjProjectIncubatorWriteRepository(ProjectIncubatorWriteRepository):
    def create(self, data: IncubatorCreatePayload) -> ProjectIncubator:
        return ProjectIncubator.objects.create(
            project_id=data.project_id.value,
            name=data.name.value,
            description=data.description.value,
        )

    def update(self, data: IncubatorUpdatePayload) -> ProjectIncubator:
        incubator: ProjectIncubator | None = ProjectIncubator.objects.filter(project_id=data.project_id.value).first()
        if incubator is None:
            raise ProjectIncubatorNotFoundException(
                f"Project with id {data.project_id.value} does not have an incubator."
            )

        if data.name is not None:
            incubator.name = data.name.value
        if data.description is not None:
            incubator.description = data.description.value

        incubator.save()
        return incubator

    def delete_by_id(self, id_: IncubatorId) -> None:
        raise NotImplementedError("The method delete_by_id() is not implemented yet.")
