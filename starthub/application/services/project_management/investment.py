from pprint import pformat

from application.ports.service import AbstractAppService
from django.db import transaction
from domain.events.project import ProjectInvestmentCreatedEvent
from domain.models.project_management.project import Project
from domain.models.user_management.user import User
from domain.repositories.project.project import ProjectReadRepository
from domain.repositories.user_management.user import UserReadRepository
from domain.services.project_management.investment import ProjectInvestmentService
from domain.value_objects.common import Id
from domain.value_objects.project.investment import (
    ProjectInvestmentCreateCommand,
    ProjectInvestmentCreatePayload,
    ProjectInvestmentId,
    ProjectInvestmentUpdateCommand,
    ProjectInvestmentUpdatePayload,
)
from infrastructure.event_bus import EventBus
from loguru import logger


class ProjectInvestmentAppService(AbstractAppService):
    def __init__(
        self,
        project_investment_service: ProjectInvestmentService,
        user_read_repository: UserReadRepository,
        project_read_repository: ProjectReadRepository,
    ):
        self._project_investment_service = project_investment_service
        self._user_read_repository = user_read_repository
        self._project_read_repository = project_read_repository

    def create(self, user_id: Id, project_id: Id, command: ProjectInvestmentCreateCommand) -> None:
        """
        :raises UserNotFoundException:
        :raises ProjectNotFoundException:
        """

        user: User = self._user_read_repository.get_by_id(id_=user_id)
        project: Project = self._project_read_repository.get_by_id(id_=project_id)
        payload = self._convert_create_command_to_payload(command=command, project_id=project_id)

        investment = self._project_investment_service.create(user=user, project=project, payload=payload)
        logger.info(f"ProjectInvestment(id={investment.id}) created successfully.")

        event = ProjectInvestmentCreatedEvent(
            user=user, project=project, project_investment=investment, social_links=command.social_links
        )
        EventBus().publish(event)

    def _convert_create_command_to_payload(
        self, command: ProjectInvestmentCreateCommand, project_id: Id
    ) -> ProjectInvestmentCreatePayload:
        return ProjectInvestmentCreatePayload(
            project_id=project_id,
            organization_name=command.organization_name,
            amount=command.amount,
        )

    def update(
        self, user_id: Id, project_id: Id, investment_id: ProjectInvestmentId, command: ProjectInvestmentUpdateCommand
    ) -> None:
        user: User = self._user_read_repository.get_by_id(id_=user_id)
        project: Project = self._project_read_repository.get_by_id(id_=project_id)

        payload = self._convert_update_command_to_payload(command=command, investmetn_id=investment_id)
        logger.debug(f"payload: \n{pformat(payload.__dict__)}")
        with transaction.atomic():
            self._project_investment_service.update(user=user, project=project, payload=payload)
            logger.info(f"ProjectInvestment with id = {investment_id.value} updated successfully.")

    def _convert_update_command_to_payload(
        self,
        command: ProjectInvestmentUpdateCommand,
        investmetn_id: ProjectInvestmentId,
    ) -> ProjectInvestmentUpdatePayload:
        return ProjectInvestmentUpdatePayload(
            investment_id=investmetn_id,
            organization_name=command.organization_name,
            amount=command.amount,
        )
