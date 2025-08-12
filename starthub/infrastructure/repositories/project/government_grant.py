from domain.models.project_management.government_grant import ProjectGovernmentGrant
from domain.repositories.project.government_grant import (
    ProjectGovernmentGrantReadRepository,
    ProjectGovernmentGrantWriteRepository,
)
from domain.value_objects.common import Pagination
from domain.value_objects.filter import ProjectGovernmentGrantFilter
from domain.value_objects.project.government_grant import (
    ProjectGovernmentGrantId,
    ProjectGovernmentGrantUpdatePayload,
    ProjectGoverntmentGrantCreatePayload,
)
from infrastructure.repositories.pagination import apply_pagination


class DjProjectGovernmentGrantReadRepository(ProjectGovernmentGrantReadRepository):
    def get_by_id(self, id_: ProjectGovernmentGrantId) -> ProjectGovernmentGrant:
        raise NotImplementedError("The method get_by_id() is not implemented yet.")

    def get_all(
        self, filter_: ProjectGovernmentGrantFilter, pagination: Pagination | None = None
    ) -> list[ProjectGovernmentGrant]:
        queryset = ProjectGovernmentGrant.objects.all()

        if filter_.project_id is not None:
            queryset = queryset.filter(project_id=filter_.project_id.value)
        if pagination:
            return apply_pagination(queryset, pagination)

        return list(queryset)


class DjProjectGovernmentGrantWriteRepository(ProjectGovernmentGrantWriteRepository):
    def create(self, data: ProjectGoverntmentGrantCreatePayload) -> ProjectGovernmentGrant:
        return ProjectGovernmentGrant.objects.create(
            project_id=data.project_id.value,
            grant_name=data.grant_name.value,
            amount=data.amount.value,
            organization_name=data.organization_name.value,
        )

    def update(self, data: ProjectGovernmentGrantUpdatePayload) -> ProjectGovernmentGrant:
        raise NotImplementedError("The method update() is not implemented yet.")

    def delete_by_id(self, id_: ProjectGovernmentGrantId) -> None:
        raise NotImplementedError("The method delete_by_id() is not implemented yet.")
