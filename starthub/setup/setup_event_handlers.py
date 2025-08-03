from application.builders.event_handler.project import (
    ProjectCreatedEventHandlerBuilder,
    ProjectDeletedEventHandlerBuilder,
)
from domain.enums.event import EventType
from infrastructure.event_bus import EventBus
from loguru import logger


def setup_event_handlers() -> None:
    logger.warning("Started setup event handlers.")
    bus = EventBus()

    project_created_handler = ProjectCreatedEventHandlerBuilder.create_handler()
    project_deleted_handler = ProjectDeletedEventHandlerBuilder.create_handler()

    bus.subscribe(event_type=EventType.Project.CREATED, handler=project_created_handler)
    bus.subscribe(event_type=EventType.Project.DELETED, handler=project_deleted_handler)

    logger.info("Event handlers successfully registered.")
