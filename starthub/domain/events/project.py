from domain.enums.event import EventType
from domain.events.base import DomainEvent
from domain.models.project_management.investment import ProjectInvestment
from domain.models.project_management.project import Project
from domain.models.user_management.user import User
from domain.value_objects.common import Id, SocialLink
from domain.value_objects.notification import NotificationMessage, NotificationTitle
from domain.value_objects.project.project import ProjectCreateCommand
from domain.value_objects.project.report import ProjectReportContent
from pydantic import Field


# ==== Project =====
class ProjectCreatedEvent(DomainEvent):
    user_id: Id
    project_id: Id
    command: ProjectCreateCommand
    event_type: EventType.Project = Field(default=EventType.Project.CREATED)


class ProjectDeletedEvent(DomainEvent):
    project_id: Id
    plan_file_path: str | None
    image_paths: list[str]

    event_type: EventType.Project = Field(default=EventType.Project.DELETED)


class ProjectApprovedNotificationEvent(DomainEvent):
    user_id: Id
    title: NotificationTitle
    message: NotificationMessage

    event_type: EventType.Project = Field(default=EventType.Project.APPROVED)


class ProjectRejectedEvent(DomainEvent):
    user_id: Id
    project_id: Id
    report: ProjectReportContent

    event_type: EventType.Project = Field(default=EventType.Project.REJECTED)


# ==== ProjectInvestment ====
class ProjectInvestmentCreatedEvent(DomainEvent):
    user: User
    project: Project
    project_investment: ProjectInvestment
    social_links: list[SocialLink]

    event_type: EventType.ProjectInvestment = Field(default=EventType.ProjectInvestment.CREATED)
