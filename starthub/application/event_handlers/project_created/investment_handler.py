from application.services.project_management.investment import ProjectInvestmentAppService
from domain.events.project import ProjectCreatedEvent
from domain.ports.event import AbstractEventHandler


class ProjectCreatedInvestmentHandler(AbstractEventHandler[ProjectCreatedEvent]):
    def __init__(self, investment_app_service: ProjectInvestmentAppService):
        self._investment_app_service = investment_app_service

    def handle(self, event: ProjectCreatedEvent) -> None:
        command = event.command
        user_id = event.user_id
        project_id = event.project_id

        if command.investment is not None:
            self._investment_app_service.create(user_id=user_id, project_id=project_id, command=command.investment)
