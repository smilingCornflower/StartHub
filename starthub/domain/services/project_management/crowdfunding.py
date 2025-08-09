from domain.models.project_management.crowdfunding import ProjectCrowdfunding
from domain.ports.service import AbstractDomainService
from domain.repositories.project.crowdfunding import ProjectCrowdfundingWriteRepository
from domain.value_objects.project.crowdfunding import ProjectCrowdfundingCreatePayload


class ProjectCrowdfundingService(AbstractDomainService):
    def __init__(
        self,
        write_repository: ProjectCrowdfundingWriteRepository,
    ):
        self._write_repository = write_repository

    def create(self, payload: ProjectCrowdfundingCreatePayload) -> ProjectCrowdfunding:
        return self._write_repository.create(data=payload)
