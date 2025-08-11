from domain.events.project import ProjectInvestmentCreatedEvent
from domain.ports.event import AbstractEventHandler


class ProjectInvestmentCreatedEventHandler(AbstractEventHandler[ProjectInvestmentCreatedEvent]):
    def handle(self, event: ProjectInvestmentCreatedEvent) -> None:
        pass
