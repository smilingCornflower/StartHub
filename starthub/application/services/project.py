from typing import Any

from application.converters.inner.company_founder_command_to_payload import convert_company_founder_command_to_payload
from application.converters.inner.project_command_to_company_create_command import (
    convert_project_create_command_to_company_create_command,
)
from application.converters.inner.project_command_to_payload import convert_project_create_command_to_payload
from application.converters.inner.team_members_create_command_to_payload import (
    convert_team_members_create_command_to_payload,
)
from application.converters.request_converters.project import (
    request_data_to_project_create_command,
    request_data_to_project_filter,
    request_data_to_the_project_update_command,
    request_files_to_project_image_create_command,
    request_project_data_to_project_images_update_command,
)
from application.converters.resposne_converters.project import project_to_dto, projects_to_dtos
from application.dto.project import ProjectDto
from application.ports.service import AbstractAppService
from django.core.files.uploadedfile import UploadedFile
from django.db import transaction
from django.http import QueryDict
from domain.models.company import Company, CompanyFounder
from domain.models.project import Project, ProjectPhone, TeamMember
from domain.services.company import CompanyFounderService, CompanyService
from domain.services.project_management import (
    ProjectImageService,
    ProjectPhoneService,
    ProjectService,
    ProjectSocialLinkService,
    TamMemberService,
)
from domain.value_objects.common import Id
from domain.value_objects.project_management import (
    ProjectCreateCommand,
    ProjectImageCreateCommand,
    ProjectImageDeleteCommand,
    ProjectImageUpdateCommand,
    ProjectPhoneCreatePayload,
    ProjectSocialLinkCreatePayload,
    ProjectUpdateCommand,
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
        company_founder_service: CompanyFounderService,
        project_image_service: ProjectImageService,
    ):
        self._project_service = project_service
        self._team_member_service = team_member_service
        self._project_phone_service = project_phone_service
        self._social_link_service = project_social_link_service
        self._company_service = company_service
        self._company_founder_service = company_founder_service
        self._project_image_service = project_image_service

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
            project: Project = self._project_service.create(convert_project_create_command_to_payload(command))
            company: Company = self._company_service.create(
                convert_project_create_command_to_company_create_command(command, project_id=Id(value=project.id))
            )

            logger.info(f"A company created successfully. Company id = {company.id}")
            founder: CompanyFounder = self._company_founder_service.create(
                convert_company_founder_command_to_payload(command.company_founder, Id(value=company.id))
            )
            logger.info(f"A company_founder created successfully. Founder id = {founder.id}")

            for member_payload in convert_team_members_create_command_to_payload(
                command.team_members, Id(value=project.id)
            ):
                team_member: TeamMember = self._team_member_service.create(member_payload)
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

    def update(self, data: dict[str, Any], files: dict[str, UploadedFile], project_id: int, user_id: int) -> None:
        update_command: ProjectUpdateCommand = request_data_to_the_project_update_command(
            data, files, project_id, user_id
        )
        logger.debug(f"update_command = {update_command}")
        with transaction.atomic():
            logger.warning("Started updating project.")
            self._project_service.update(update_command)
            logger.info("Project updated successfully.")

    def delete(self, project_id: int, user_id: int) -> None:
        logger.debug(f"project_id = {project_id}, user_id = {user_id}")
        self._project_service.delete(Id(value=project_id), Id(value=user_id))

    def get_plan_url(self, project_id: int) -> str:
        return self._project_service.get_plan_url(Id(value=project_id))

    def upload_project_image(self, files: dict[str, UploadedFile], project_id: int, user_id: int) -> None:
        image_create_command: ProjectImageCreateCommand = request_files_to_project_image_create_command(
            files=files, project_id=project_id, user_id=user_id
        )
        self._project_image_service.create(image_create_command)
        logger.info("ProjectImage created successfully.")

    def get_image_urls(self, project_id: int) -> list[str]:
        """:raises ProjectNotFoundException:"""

        logger.info(f"Get image urls for project with id = {project_id}")
        return self._project_image_service.get_urls(project_id=Id(value=project_id))

    def delete_image(self, project_id: int, image_order: int, user_id: int) -> None:
        logger.info(f"Deleting image. project_id: {project_id}, image_order: {image_order}")
        self._project_image_service.delete(
            command=ProjectImageDeleteCommand(
                project_id=Id(value=project_id), image_order=image_order, user_id=Id(value=user_id)
            )
        )
        logger.info(f"Image deleted successfully. project_id: {project_id}, image_order: {image_order}")

    def update_project_images(self, request_data: dict[str, Any], project_id: int, user_id: int) -> None:
        image_update_command: ProjectImageUpdateCommand = request_project_data_to_project_images_update_command(
            request_data, project_id=project_id, user_id=user_id
        )
        logger.debug(f"{image_update_command=}")
        self._project_image_service.update(image_update_command)
