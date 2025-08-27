from domain.exceptions.project_management import ProjectGovernmentGrantNotFoundException
from domain.models.project_management.government_grant import ProjectGovernmentGrant
from domain.repositories.project.government_grant import (
    ProjectGovernmentGrantReadRepository,
    ProjectGovernmentGrantWriteRepository,
)
from domain.value_objects.common import CursorPagination, OffsetPagination
from domain.value_objects.filter import ProjectGovernmentGrantFilter
from domain.value_objects.project.government_grant import (
    ProjectGovernmentGrantId,
    ProjectGovernmentGrantUpdatePayload,
    ProjectGoverntmentGrantCreatePayload,
)
from infrastructure.repositories.pagination import apply_pagination


class DjProjectGovernmentGrantReadRepository(ProjectGovernmentGrantReadRepository):
    def get_by_id(self, id_: ProjectGovernmentGrantId) -> ProjectGovernmentGrant:
        """:raises ProjectGovernmentGrantNotFoundException:"""
        grant: ProjectGovernmentGrant | None = ProjectGovernmentGrant.objects.filter(id=id_.value).first()
        if grant is None:
            raise ProjectGovernmentGrantNotFoundException(f"Government grant with id = {id_.value} not found.")
        return grant

    def get_all(
        self, filter_: ProjectGovernmentGrantFilter, pagination: CursorPagination | OffsetPagination | None = None
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
        """:raises ProjectGovernmentGrantNotFoundException:"""

        government_grant: ProjectGovernmentGrant | None = ProjectGovernmentGrant.objects.filter(
            id=data.government_grant_id.value
        ).first()
        if government_grant is None:
            raise ProjectGovernmentGrantNotFoundException(
                f"Government grant with id = {data.government_grant_id.value} not found."
            )

        if data.grant_name is not None:
            government_grant.grant_name = data.grant_name.value
        if data.amount is not None:
            government_grant.amount = data.amount.value
        if data.organization_name is not None:
            government_grant.organization_name = data.organization_name.value

        government_grant.save()
        return government_grant

    def delete_by_id(self, id_: ProjectGovernmentGrantId) -> None:
        raise NotImplementedError("The method delete_by_id() is not implemented yet.")

    def delete(self, government_grant: ProjectGovernmentGrant) -> None:
        government_grant.delete()
