from application.services.project_management.crowdfunding import CrowdfundingAppService
from domain.events.project import ProjectCreatedEvent
from domain.ports.event import AbstractEventHandler


class ProjectCreatedCrowdfundingHandler(AbstractEventHandler[ProjectCreatedEvent]):
    def __init__(
        self,
        crowdfunding_app_service: CrowdfundingAppService,
    ):
        self._crowdfunding_app_service = crowdfunding_app_service

    def handle(self, event: ProjectCreatedEvent) -> None:
        command = event.command
        user_id = event.user_id
        project_id = event.project_id

        if command.crowdunding is not None:
            self._crowdfunding_app_service.create(user_id=user_id, project_id=project_id, command=command.crowdunding)
