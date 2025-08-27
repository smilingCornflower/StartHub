from enum import StrEnum


class EventType:
    class Project(StrEnum):
        CREATED = "project_created"
        DELETED = "project_deleted"
        APPROVED = "project_approved"
        REJECTED = "project_rejected"

    class ProjectInvestment(StrEnum):
        CREATED = "project_investment_created"

    class News(StrEnum):
        CREATED = "news_created"


AnyEventType = EventType.Project | EventType.ProjectInvestment | EventType.News
