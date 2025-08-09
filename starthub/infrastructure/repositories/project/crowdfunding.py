from domain.models.project_management.crowdfunding import ProjectCrowdfunding
from domain.repositories.project.crowdfunding import (
    ProjectCrowdfundingReadRepository,
    ProjectCrowdfundingWriteRepository,
)
from domain.value_objects.common import Pagination
from domain.value_objects.filter import ProjectCrowdfundingFilter
from domain.value_objects.project.crowdfunding import (
    ProjectCrowdfundingCreatePayload,
    ProjectCrowdfundingId,
    ProjectCrowdfundingUpdatePayload,
)
from infrastructure.repositories.pagination import apply_pagination


class DjProjectCrowdfundingWriteRepository(ProjectCrowdfundingWriteRepository):
    def create(self, data: ProjectCrowdfundingCreatePayload) -> ProjectCrowdfunding:
        return ProjectCrowdfunding.objects.create(
            project_id=data.project_id.value,
            name=data.name.value,
            amount=data.amount.value,
        )

    def update(self, data: ProjectCrowdfundingUpdatePayload) -> ProjectCrowdfunding:
        raise NotImplementedError("The method update() is not implemented yet.")

    def delete_by_id(self, id_: ProjectCrowdfundingId) -> None:
        raise NotImplementedError("The method delete_by_id() is not implemented yet.")


class DjProjectCrowdFundingReadRepository(ProjectCrowdfundingReadRepository):
    def get_by_id(self, id_: ProjectCrowdfundingId) -> ProjectCrowdfunding:
        raise NotImplementedError("The method get_by_id() is not implemented yet.")

    def get_all(
        self, filter_: ProjectCrowdfundingFilter, pagination: Pagination | None = None
    ) -> list[ProjectCrowdfunding]:
        queryset = ProjectCrowdfunding.objects.all()

        if filter_.project_id is not None:
            queryset = queryset.filter(project_id=filter_.project_id.value)
        if pagination:
            return apply_pagination(queryset, pagination=pagination)

        return list(queryset)
