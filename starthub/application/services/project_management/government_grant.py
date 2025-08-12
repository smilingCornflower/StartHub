from application.ports.service import AbstractAppService
from domain.constants import PROJECT_GOVERNMENT_GRANT_MAX_AMOUNT
from domain.exceptions.project_management import ProjectGovernmentGrantMaxAmountException
from domain.models.project_management.government_grant import ProjectGovernmentGrant
from domain.models.project_management.project import Project
from domain.models.user import User
from domain.repositories.project.government_grant import ProjectGovernmentGrantReadRepository
from domain.repositories.project.project import ProjectReadRepository
from domain.repositories.user import UserReadRepository
from domain.services.project_management.government_grant import ProjectGovernmentGrantService
from domain.value_objects.common import Id
from domain.value_objects.filter import ProjectGovernmentGrantFilter
from domain.value_objects.project.government_grant import (
    ProjectGovernmentGrantId,
    ProjectGovernmentGrantUpdatePayload,
    ProjectGoverntmentGrantCreateCommand,
    ProjectGoverntmentGrantCreatePayload,
    ProjectGoverntmentGrantUpdateCommand,
)
from loguru import logger


class GovernmentGrantAppService(AbstractAppService):
    def __init__(
        self,
        government_grant_service: ProjectGovernmentGrantService,
        user_read_repository: UserReadRepository,
        project_read_repository: ProjectReadRepository,
        government_grant_read_repository: ProjectGovernmentGrantReadRepository,
    ):
        self._government_grant_service = government_grant_service
        self._user_read_repository = user_read_repository
        self._project_read_repository = project_read_repository
        self._government_grant_read_repository = government_grant_read_repository

    def create(self, user_id: Id, project_id: Id, command: ProjectGoverntmentGrantCreateCommand) -> None:
        """
        :raises ProjectGovernmentGrantMaxAmountException:
        :raises UserNotFoundException:
        :raises ProjectNotFoundException:
        """
        self._check_grants_max_amount(project_id=project_id)
        user: User = self._user_read_repository.get_by_id(id_=user_id)
        project: Project = self._project_read_repository.get_by_id(id_=project_id)
        payload = self._convert_create_command_to_payload(command=command, project_id=project_id)

        grant: ProjectGovernmentGrant = self._government_grant_service.create(
            user=user, project=project, payload=payload
        )
        logger.info(f"{grant.__class__.__name__}(id={grant.id}) created successfully.")

    def update(
        self, user_id: Id, government_grant_id: ProjectGovernmentGrantId, command: ProjectGoverntmentGrantUpdateCommand
    ) -> None:
        """
        :raises UserNotFoundException:
        :raises ProjectNotFoundException:
        :raises ProjectGovernmentGrantNotFoundException:
        """
        government_grant: ProjectGovernmentGrant = self._government_grant_read_repository.get_by_id(
            id_=government_grant_id
        )
        user: User = self._user_read_repository.get_by_id(id_=user_id)
        payload: ProjectGovernmentGrantUpdatePayload = self._convert_update_command_to_payload(
            command=command, government_grant_id=government_grant_id
        )

        self._government_grant_service.update(user=user, government_grant=government_grant, payload=payload)
        logger.info("Government grant updated successfully.")

    def delete(self, user_id: Id, government_grant_id: ProjectGovernmentGrantId) -> None:
        """
        :raises UserNotFoundException:
        :raises ProjectGovernmentGrantNotFoundException:
        """
        user: User = self._user_read_repository.get_by_id(id_=user_id)
        government_grant: ProjectGovernmentGrant = self._government_grant_read_repository.get_by_id(
            id_=government_grant_id
        )
        self._government_grant_service.delete(user=user, government_grant=government_grant)
        logger.info(f"GovernmentGrant(id={government_grant_id.value}) deleted successfully.")

    def _convert_create_command_to_payload(
        self, command: ProjectGoverntmentGrantCreateCommand, project_id: Id
    ) -> ProjectGoverntmentGrantCreatePayload:
        return ProjectGoverntmentGrantCreatePayload(
            project_id=project_id,
            grant_name=command.grant_name,
            organization_name=command.organization_name,
            amount=command.amount,
        )

    def _convert_update_command_to_payload(
        self, command: ProjectGoverntmentGrantUpdateCommand, government_grant_id: ProjectGovernmentGrantId
    ) -> ProjectGovernmentGrantUpdatePayload:
        return ProjectGovernmentGrantUpdatePayload(
            government_grant_id=government_grant_id,
            grant_name=command.grant_name,
            organization_name=command.organization_name,
            amount=command.amount,
        )

    def _check_grants_max_amount(self, project_id: Id) -> None:
        """:raises ProjectGovernmentGrantMaxAmountException:"""

        grants: list[ProjectGovernmentGrant] = self._government_grant_read_repository.get_all(
            filter_=ProjectGovernmentGrantFilter(project_id=project_id)
        )
        if not (len(grants) < PROJECT_GOVERNMENT_GRANT_MAX_AMOUNT):
            raise ProjectGovernmentGrantMaxAmountException(
                f"Project with id = {project_id.value} already has the maximum allowed number of government grants ({PROJECT_GOVERNMENT_GRANT_MAX_AMOUNT})."
            )
        return None
