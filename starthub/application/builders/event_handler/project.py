from typing import Any

from application.builders.domain_service.address import AddressServiceBuilder
from application.builders.domain_service.project_management import (
    CompanyFounderServiceBuilder,
    CompanyServiceBuilder,
    ProjectImageServiceBuilder,
    ProjectPhoneServiceBuilder,
    ProjectSocialLinkServiceBuilder,
    ProjectStepServiceBuilder,
    TeamMemberServiceBuilder,
)
from application.event_handlers.project_created_handler import ProjectCreatedEventHandler
from application.event_handlers.project_deleted_handler import ProjectDeletedEventHandler
from application.ports.event_handler_builder import AbstractEventHandlerBuilder
from domain.events.project import ProjectCreatedEvent, ProjectDeletedEvent
from domain.ports.event import AbstractEventHandler
from infrastructure.cloud_storages.google import google_cloud_storage


class ProjectCreatedEventHandlerBuilder(AbstractEventHandlerBuilder[Any]):
    @staticmethod
    def create_handler() -> AbstractEventHandler[ProjectCreatedEvent]:
        return ProjectCreatedEventHandler(
            company_service=CompanyServiceBuilder.create_service(),
            company_founder_service=CompanyFounderServiceBuilder.create_service(),
            project_image_service=ProjectImageServiceBuilder.create_service(),
            team_member_service=TeamMemberServiceBuilder.create_service(),
            project_phone_service=ProjectPhoneServiceBuilder.create_service(),
            social_link_service=ProjectSocialLinkServiceBuilder.create_service(),
            address_service=AddressServiceBuilder.create_service(),
            project_step_service=ProjectStepServiceBuilder.create_service(),
        )


class ProjectDeletedEventHandlerBuilder(AbstractEventHandlerBuilder[Any]):
    @staticmethod
    def create_handler() -> AbstractEventHandler[ProjectDeletedEvent]:
        return ProjectDeletedEventHandler(
            cloud_storage=google_cloud_storage,
        )
