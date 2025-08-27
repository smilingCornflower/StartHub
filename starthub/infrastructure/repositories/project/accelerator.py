from domain.exceptions.project_management import ProjectAcceleratorNotFoundException
from domain.models.project_management.accelerator import ProjectAccelerator
from domain.repositories.project.accelerator import ProjectAcceleratorReadRepository, ProjectAcceleratorWriteRepository
from domain.value_objects.common import CursorPagination, OffsetPagination
from domain.value_objects.filter import ProjectAcceleratorFilter
from domain.value_objects.project.accelerator import (
    AcceleratorId,
    ProjectAcceleratorCreatePayload,
    ProjectAcceleratorUpdatePayload,
)
from infrastructure.repositories.pagination import apply_pagination


class DjProjectAcceleratorReadRepository(ProjectAcceleratorReadRepository):
    def get_by_id(self, id_: AcceleratorId) -> ProjectAccelerator:
        accelerator: ProjectAccelerator | None = ProjectAccelerator.objects.filter(id=id_.value).first()
        if accelerator is None:
            raise ProjectAcceleratorNotFoundException(f"Project accelerator with id = {id_.value} not found.")
        return accelerator

    def get_all(
        self, filter_: ProjectAcceleratorFilter, pagination: CursorPagination | OffsetPagination | None = None
    ) -> list[ProjectAccelerator]:
        queryset = ProjectAccelerator.objects.all()
        if filter_.project_id is not None:
            queryset = queryset.filter(project_id=filter_.project_id.value)

        if pagination is not None:
            return apply_pagination(queryset=queryset, pagination=pagination)
        return list(queryset)


class DjProjectAcceleratorWriteRepository(ProjectAcceleratorWriteRepository):
    def create(self, data: ProjectAcceleratorCreatePayload) -> ProjectAccelerator:
        return ProjectAccelerator.objects.create(
            project_id=data.project_id.value,
            name=data.name.value,
            description=data.name.value,
        )

    def update(self, data: ProjectAcceleratorUpdatePayload) -> ProjectAccelerator:
        accelerator: ProjectAccelerator | None = ProjectAccelerator.objects.filter(
            project_id=data.project_id.value
        ).first()

        if accelerator is None:
            raise ProjectAcceleratorNotFoundException(
                f"Project with id {data.project_id.value} does not have an accelerator."
            )

        if data.name is not None:
            accelerator.name = data.name.value
        if data.description is not None:
            accelerator.description = data.description.value

        accelerator.save()
        return accelerator

    def delete_by_id(self, id_: AcceleratorId) -> None:
        raise NotImplementedError("The method delete_by_id() is not implemented yet.")

    def delete(self, accelerator: ProjectAccelerator) -> None:
        accelerator.delete()
