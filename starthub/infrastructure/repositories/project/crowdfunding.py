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
        raise NotImplementedError("The method get_all() is not implemented yet.")
