from domain.events.project import ProjectCreatedEvent
from domain.models.project_management.step import ProjectStep
from domain.ports.event import AbstractEventHandler
from domain.services.project_management.step import ProjectStepService
from domain.value_objects.project.step import ProjectStepCreatePaylaod
from loguru import logger


class ProjectCreatedProjectStepsHandler(AbstractEventHandler[ProjectCreatedEvent]):
    def __init__(self, project_step_service: ProjectStepService):
        self._project_step_service = project_step_service

    def handle(self, event: ProjectCreatedEvent) -> None:
        command = event.command
        project_id = event.project_id

        for project_step_create_command in command.steps:
            payload = ProjectStepCreatePaylaod(
                project_id=project_id,
                name=project_step_create_command.name,
                description=project_step_create_command.description,
                date=project_step_create_command.date,
            )
            project_step: ProjectStep = self._project_step_service.create(paylaod=payload)
            logger.debug(f"project_step with id = {project_step.id} created successfully")
