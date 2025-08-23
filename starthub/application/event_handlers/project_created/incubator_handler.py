from loguru import logger

from domain.events.project import ProjectCreatedEvent
from domain.ports.event import AbstractEventHandler
from domain.services.project_management.incubator import IncubatorService
from domain.value_objects.project.incubator import IncubatorCreatePayload


class ProjectCreatedIncubatorHandler(AbstractEventHandler[ProjectCreatedEvent]):
    def __init__(self, incubator_service: IncubatorService):
        self._incubator_service = incubator_service

    def handle(self, event: ProjectCreatedEvent) -> None:
        command = event.command
        project_id = event.project_id
        if command.incubator is not None:
            payload = IncubatorCreatePayload(
                project_id=project_id,
                name=command.incubator.name,
                description=command.incubator.description,
            )
            self._incubator_service.create(payload=payload)
            logger.info("Project incubator created successfully.")
