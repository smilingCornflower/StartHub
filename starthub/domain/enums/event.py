from enum import StrEnum


class EventType:
    class Project(StrEnum):
        CREATED = "project_created"
        DELETED = "project_deleted"

    class ProjectInvestment(StrEnum):
        CREATED = "project_investment_created"


AnyEventType = EventType.Project | EventType.ProjectInvestment
