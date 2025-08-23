from loguru import logger

from domain.events.project import ProjectCreatedEvent
from domain.models import ProjectPhone
from domain.ports.event import AbstractEventHandler
from domain.services.project_management.project_phone import ProjectPhoneService
from domain.value_objects.project.phone import ProjectPhoneCreatePayload


class ProjectCreatedPhoneHandler(AbstractEventHandler[ProjectCreatedEvent]):
    def __init__(self, project_phone_service: ProjectPhoneService):
        self._project_phone_service = project_phone_service

    def handle(self, event: ProjectCreatedEvent) -> None:
        command = event.command
        project_id = event.project_id

        project_phone: ProjectPhone = self._project_phone_service.create(
            ProjectPhoneCreatePayload(project_id=project_id, number=command.phone_number)
        )
        logger.debug(f"project_phone with id = {project_phone.id} created successfully.")
