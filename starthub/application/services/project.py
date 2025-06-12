from typing import Any

from application.converters.inner.project_command_to_payload import convert_project_create_command_to_payload
from application.converters.request_converters.project import (
    request_data_to_project_create_command,
    request_data_to_project_filter,
)
from application.converters.resposne_converters.project import project_to_dto, projects_to_dtos
from application.dto.project import ProjectDto
from application.ports.service import AbstractAppService
from django.core.files.uploadedfile import UploadedFile
from django.db import transaction
from django.http import QueryDict
from domain.models.company import Company
from domain.models.project import Project, ProjectPhone, TeamMember
from domain.services.company import CompanyService
from domain.services.project_management import (
    ProjectPhoneService,
    ProjectService,
    ProjectSocialLinkService,
    TamMemberService,
)
from domain.value_objects.common import Id
from domain.value_objects.project_management import (
    ProjectCreateCommand,
    ProjectPhoneCreatePayload,
    ProjectSocialLinkCreatePayload,
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
        company_service: CompanyService,
    ):
        self._project_service = project_service
        self._team_member_service = team_member_service
        self._project_phone_service = project_phone_service
        self._social_link_service = project_social_link_service
        self._company_service = company_service

    def get_by_id(self, project_id: int) -> ProjectDto:
        """:raises ProjectNotFoundException:"""
        return project_to_dto(self._project_service.get_by_id(Id(value=project_id)))

    def get(self, data: QueryDict) -> list[ProjectDto]:
        project_filter = request_data_to_project_filter(data)
        logger.debug(f"project_filter = {project_filter}")

        project: list[Project] = self._project_service.get(project_filter)
        return projects_to_dtos(project)

    def create(self, data: dict[str, Any], files: dict[str, UploadedFile], user_id: int) -> Project:
        logger.warning("Started creating project.")
        logger.debug(f"{data=}")

        command: ProjectCreateCommand = request_data_to_project_create_command(data, files, user_id)
        logger.debug(f"Command = {command}")

        with transaction.atomic():
            company: Company = self._company_service.create(command=command.company)
            logger.info(f"A company created successfully. Company id = {company.id}")

            project: Project = self._project_service.create(
                convert_project_create_command_to_payload(command, company.id)
            )

            for member in command.team_members:
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
                ProjectPhoneCreatePayload(project_id=Id(value=project.id), number=command.phone_number)
            )
            logger.info(f"project_phone with id = {project_phone.id} created successfully.")

            for social_link in command.social_links:
                logger.debug(f"Creating social_link: {social_link}.")
                self._social_link_service.create(
                    ProjectSocialLinkCreatePayload(project_id=Id(value=project.id), social_link=social_link)
                )
                logger.debug("social link created successfully.")
            logger.info("All social links create successfully.")

        return project

    def delete(self, project_id: int, user_id: int) -> None:
        logger.debug(f"project_id = {project_id}, user_id = {user_id}")
        self._project_service.delete(Id(value=project_id), Id(value=user_id))

    def get_plan_url(self, project_id: int) -> str:
        return self._project_service.get_plan_url(Id(value=project_id))
