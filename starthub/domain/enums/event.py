from enum import StrEnum


class EventType:
    class Project(StrEnum):
        CREATED = "project_created"
        DELETED = "project_deleted"


AnyEventType = EventType.Project
