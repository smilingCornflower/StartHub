from typing import Any

from application.converters.request_converters.project import (
    request_data_to_project_create_payload,
    request_data_to_project_filter,
    request_data_to_project_update_payload,
)
from application.converters.resposne_converters.project import project_to_dto, projects_to_dtos
from application.dto.project import ProjectDto
from application.ports.service import AbstractAppService
from django.db import transaction
from django.http import QueryDict

from domain.exceptions.project_management import InvalidProjectStageException
from domain.models.project import Project, ProjectPhone, TeamMember
from domain.services.project_management import (
    ProjectPhoneService,
    ProjectService,
    ProjectSocialLinkService,
    TamMemberService,
)
from domain.value_objects.common import Id
from domain.value_objects.project_management import (
    ProjectCreatePayload,
    ProjectPhoneCreatePayload,
    ProjectSocialLinkCreatePayload,
    ProjectUpdatePayload,
    TeamMemberCreatePayload,
)
from loguru import logger


class ProjectAppService(AbstractAppService):
    def __init__(
        self,
        project_service: ProjectService,
        team_member_service: TamMemberService,
        project_phone_service: ProjectPhoneService,
        project_social_link_service: ProjectSocialLinkService,
    ):
        self._project_service = project_service
        self._team_member_service = team_member_service
        self._project_phone_service = project_phone_service
        self._social_link_service = project_social_link_service

    def get_by_id(self, project_id: int) -> ProjectDto:
        """:raises ProjectNotFoundException:"""
        return project_to_dto(self._project_service.get_by_id(Id(value=project_id)))

    def get(self, data: QueryDict) -> list[ProjectDto]:
        project_filter = request_data_to_project_filter(data)
        logger.debug(f"project_filter = {project_filter}")

        project: list[Project] = self._project_service.get(project_filter)
        return projects_to_dtos(project)

    def create(self, data: dict[str, Any], user_id: int) -> Project:
        """
        Creates a new project with the given data and associates it with the user.

        Args:
            data (dict): A dictionary containing required project fields:
                - name (str): Project name.
                - description (str): Project description.
                - category_id (int): Project category ID.
                - funding_model_id (int): Funding model ID.
                - goal_sum (int): Target funding amount.
                - deadline (str): Project deadline date in "YYYY-MM-DD" format.
                - team_members (list): List of team members, each a dict with:
                    * first_name (str) — member's first name,
                    * last_name (str) — member's last name,
                    * description (str) — member's description.
                - company_id (int): Company ID owning the project.
                - social_links (dict): Social platform keys with URL values.
                - phone_number (str): Contact phone number.

            user_id (int): ID of the user creating the project. Must be a company representative.

        Returns:
            Project: The created project instance.

        Raises:
            KeyError: If required fields are missing in data.
            ProjectNameIsTooLongValidationException: If the project name is too long.
            EmptyStringException: If any required string field is empty.
            NegativeProjectGoalSumValidationException: If goal_sum is negative.
            ProjectDeadlineInPastValidationException: If deadline is in the past.
            DateIsNoIsoFormatException: If deadline date format is invalid.
            ProjectCategoryNotFoundException: If project category does not exist.
            FundingModelNotFoundException: If funding model does not exist.
            InvalidProjectStageException: If value is not allowed. Valid values: idea, mvp, scale, validation, prototype
            CompanyNotFoundException: If company does not exist.
            InvalidPhoneNumberException: If phone number is invalid.
            InvalidSocialLinkException: If any social link is invalid.
            DisallowedSocialLinkException: If social platform is not allowed.
            FirstNameIsTooLongException: If a team member's first name is too long.
            LastNameIsTooLongException: If a team member's last name is too long.
            UserNotFoundException: If user with user_id does not exist.
            CompanyOwnershipRequiredException: If user is not a company representative.

        Notes:
            - Project creation and related objects are created within a single transaction.
            - On validation failure, the transaction is rolled back and no objects are created.
        """
        logger.warning("Started creating project.")
        logger.debug(f"{data=}")

        payload: ProjectCreatePayload = request_data_to_project_create_payload(data, user_id)
        logger.debug(f"Payload = {payload}")

        with transaction.atomic():
            project: Project = self._project_service.create(payload=payload)
            logger.info(f"A project created successfully. Project id = {project.id}")

            for member in payload.team_members:
                create_payload = TeamMemberCreatePayload(
                    project_id=Id(value=project.id),
                    first_name=member.first_name,
                    last_name=member.last_name,
                    description=member.description,
                )
                team_member: TeamMember = self._team_member_service.create(create_payload)
                logger.debug(f"Team member with id = {team_member.id} is attached to the project successfully.")
            logger.info("All team members were created successfully.")

            project_phone: ProjectPhone = self._project_phone_service.create(
                ProjectPhoneCreatePayload(project_id=Id(value=project.id), number=payload.phone_number)
            )
            logger.info(f"project_phone with id = {project_phone.id} created successfully.")

            for social_link in payload.social_links:
                logger.debug(f"Creating social_link: {social_link}.")
                self._social_link_service.create(
                    ProjectSocialLinkCreatePayload(project_id=Id(value=project.id), social_link=social_link)
                )
                logger.debug("social link created successfully.")
            logger.info("All social links create successfully.")

        return project

    def update(self, data: dict[str, Any], project_id: int, user_id: int) -> Project:
        logger.info("Started updating project.")
        logger.debug(f"user_id = {user_id}; data = {data}")

        project_update_payload: ProjectUpdatePayload = request_data_to_project_update_payload(data, project_id)
        logger.debug(f"project_update_payload = {project_update_payload}")

        project_updated: Project = self._project_service.update(project_update_payload, Id(value=user_id))
        return project_updated

    def delete(self, project_id: int, user_id: int) -> None:
        logger.debug(f"project_id = {project_id}, user_id = {user_id}")
        self._project_service.delete(Id(value=project_id), Id(value=user_id))
