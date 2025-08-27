from domain.models.project_management.step import ProjectStep
from domain.repositories.project.step import ProjectStepReadRepository, ProjectStepWriteRepository
from domain.value_objects.common import CursorPagination, Id, OffsetPagination
from domain.value_objects.filter import ProjectStepFilter
from domain.value_objects.project.step import ProjectStepCreatePaylaod, ProjectStepId, ProjectStepUpdatePayload
from infrastructure.repositories.pagination import apply_pagination


class DjProjectStepReadRepository(ProjectStepReadRepository):
    def get_by_id(self, id_: ProjectStepId) -> ProjectStep:
        raise NotImplementedError("The method get_by_id() is not implemented yet.")

    def get_all(
        self, filter_: ProjectStepFilter, pagination: CursorPagination | OffsetPagination | None = None
    ) -> list[ProjectStep]:
        queryset = ProjectStep.objects.all()

        if filter_.project_id is not None:
            queryset = queryset.filter(project_id=filter_.project_id.value)

        if pagination:
            return apply_pagination(queryset=queryset, pagination=pagination)

        return list(queryset)


class DjProjectStepWriteRepositroy(ProjectStepWriteRepository):
    def create(self, data: ProjectStepCreatePaylaod) -> ProjectStep:
        return ProjectStep.objects.create(
            project_id=data.project_id.value,
            name=data.name.value,
            description=data.description.value,
            date=data.date.value,
        )

    def update(self, data: ProjectStepUpdatePayload) -> ProjectStep:
        raise NotImplementedError("The method update() is not implemented yet.")

    def delete_by_id(self, id_: Id) -> None:
        raise NotImplementedError("The method delete_by_id() is not implemented yet.")
