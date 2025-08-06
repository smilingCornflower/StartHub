from domain.enums.event import EventType
from domain.events.base import DomainEvent
from domain.value_objects.common import Id
from domain.value_objects.project.project import ProjectCreateCommand
from pydantic import Field


class ProjectCreatedEvent(DomainEvent):
    project_id: Id
    command: ProjectCreateCommand
    event_type: EventType.Project = Field(default=EventType.Project.CREATED)


class ProjectDeletedEvent(DomainEvent):
    project_id: Id
    plan_file_path: str | None
    image_paths: list[str]

    event_type: EventType.Project = Field(default=EventType.Project.DELETED)
