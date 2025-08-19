from application.ports.service import AbstractAppService
from domain.exceptions.project_management import ProjectUsefulLinkAlreadyExistsException
from domain.models.project_management.project import Project
from domain.models.project_management.useful_link import ProjectUsefulLink
from domain.models.user import User
from domain.repositories.project.project import ProjectReadRepository
from domain.repositories.project.useful_link import ProjectUsefulLinkReadRepository
from domain.repositories.user import UserReadRepository
from domain.services.project_management.useful_link import ProjectUsefulLinkService
from domain.value_objects.common import Id
from domain.value_objects.filter import ProjectUsefulLinkFilter
from domain.value_objects.project.useful_link import (
    UsefulLinkCreateCommand,
    UsefulLinkCreatePayload,
    UsefulLinkId,
    UsefulLinkUpdateCommand,
    UsefulLinkUpdatePayload,
)


class ProjectUsefulLinkAppService(AbstractAppService):
    def __init__(
        self,
        service: ProjectUsefulLinkService,
        useful_link_read_repository: ProjectUsefulLinkReadRepository,
        user_read_repository: UserReadRepository,
        project_read_repository: ProjectReadRepository,
    ):
        self._service = service
        self._useful_link_read_repository = useful_link_read_repository
        self._user_read_repository = user_read_repository
        self._project_read_repository = project_read_repository

    # ==== CREATE ======================================================================================================
    def create(self, user_id: Id, project_id: Id, command: UsefulLinkCreateCommand) -> None:
        self._check_dublicate_links(project_id=project_id, link=command.url)

        user: User = self._user_read_repository.get_by_id(id_=user_id)
        project: Project = self._project_read_repository.get_by_id(id_=project_id)
        payload = self._convert_create_command_to_payload(command=command, project_id=project_id)

        self._service.create(user=user, project=project, payload=payload)

    def _check_dublicate_links(self, project_id: Id, link: str) -> None:
        """:raises ProjectUsefulLinkAlreadyExistsException:"""
        search_result = self._useful_link_read_repository.get_all(
            filter_=ProjectUsefulLinkFilter(project_id=project_id, useful_link=link)
        )
        if search_result:
            raise ProjectUsefulLinkAlreadyExistsException("This link already exists for this project.")

        return None

    def _convert_create_command_to_payload(
        self, command: UsefulLinkCreateCommand, project_id: Id
    ) -> UsefulLinkCreatePayload:
        return UsefulLinkCreatePayload(
            project_id=project_id,
            name=command.name,
            url=command.url,
        )

    # ==== UPDATE ======================================================================================================
    def update(self, user_id: Id, useful_link_id: UsefulLinkId, command: UsefulLinkUpdateCommand) -> None:
        user = self._user_read_repository.get_by_id(id_=user_id)
        link = self._useful_link_read_repository.get_by_id(id_=useful_link_id)
        payload = self._convert_update_command_to_payload(command=command, useful_link_id=useful_link_id)

        self._service.update(user=user, useful_link=link, payload=payload)

    def _convert_update_command_to_payload(
        self, command: UsefulLinkUpdateCommand, useful_link_id: UsefulLinkId
    ) -> UsefulLinkUpdatePayload:
        return UsefulLinkUpdatePayload(
            useful_link_id=useful_link_id,
            name=command.name,
            url=command.url,
        )

    # ==== DELETE ======================================================================================================
    def delete(self, user_id: Id, useful_link_id: UsefulLinkId) -> None:
        user: User = self._user_read_repository.get_by_id(id_=user_id)
        link: ProjectUsefulLink = self._useful_link_read_repository.get_by_id(id_=useful_link_id)

        self._service.delete(user=user, useful_link=link)
