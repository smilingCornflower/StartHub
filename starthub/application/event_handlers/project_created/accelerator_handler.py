from application.services.project_management.accelerator import AcceleratorAppService
from domain.events.project import ProjectCreatedEvent
from domain.ports.event import AbstractEventHandler


class ProjectCreatedAcceleratorHandler(AbstractEventHandler[ProjectCreatedEvent]):
    def __init__(self, accelerator_app_service: AcceleratorAppService):
        self._accelerator_app_service = accelerator_app_service

    def handle(self, event: ProjectCreatedEvent) -> None:
        command = event.command
        user_id = event.user_id
        project_id = event.project_id
        if command.accelerator is not None:
            self._accelerator_app_service.create(user_id=user_id, project_id=project_id, command=command.accelerator)
