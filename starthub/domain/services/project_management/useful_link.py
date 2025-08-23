from loguru import logger

from domain.constants import USEFUL_LINKS_MAX_AMOUNT
from domain.enums.permission import ActionEnum, ScopeEnum
from domain.exceptions.permissions import (
    AddDeniedPermissionException,
    DeleteDeniedPermissionException,
    UpdateDeniedPermissionException,
)
from domain.exceptions.project_management import ProjectUsefulLinkMaxAmountException
from domain.models.project_management.project import Project
from domain.models.project_management.useful_link import ProjectUsefulLink
from domain.models.user import User
from domain.ports.service import AbstractDomainService
from domain.repositories.project.useful_link import ProjectUsefulLinkReadRepository, ProjectUsefulLinkWriteRepository
from domain.services.permission import PermissionService
from domain.value_objects.common import Id
from domain.value_objects.filter import ProjectUsefulLinkFilter
from domain.value_objects.project.useful_link import UsefulLinkCreatePayload, UsefulLinkUpdatePayload


class UsefulLinkPermissionService(AbstractDomainService):
    def __init__(self, permission_service: PermissionService):
        self._permission_service = permission_service

    def _check_create_permission(self, user: User, project: Project) -> None:
        """:raises AddDeniedPermissionException:"""
        create_permission = self._permission_service.create_permission_vo(
            model=ProjectUsefulLink,
            action=ActionEnum.ADD,
            scope=ScopeEnum.OWN,
        )
        has_permission = self._permission_service.has_user_permission(user=user, permission_vo=create_permission)
        if has_permission and project.creator == user:
            return None
        else:
            logger.exception(
                f"User(id={user.id}) doesn't have enough permissions to add ProjectUsefulLink to the Project(id={project.id})."
            )
            raise AddDeniedPermissionException("You don't have enough permissions to add this resource.")

    def _check_update_permission(self, user: User, useful_link: ProjectUsefulLink) -> None:
        """:raises UpdateDeniedPermissionException:"""

        update_permission = self._permission_service.create_permission_vo(
            model=ProjectUsefulLink,
            action=ActionEnum.CHANGE,
            scope=ScopeEnum.OWN,
        )
        has_permission = self._permission_service.has_user_permission(user=user, permission_vo=update_permission)

        if has_permission and useful_link.project.creator == user:
            return None
        else:
            logger.exception(
                f"User(id={user.id}) doesn't have enough permissions to update ProjectUsefulLink(id={useful_link.id})."
            )
        raise UpdateDeniedPermissionException("You don't have enough permissions to change this resource.")

    def _check_delete_permission(self, user: User, useful_link: ProjectUsefulLink) -> None:
        """:raises DeleteDeniedPermissionException:"""

        delete_permission = self._permission_service.create_permission_vo(
            model=ProjectUsefulLink,
            action=ActionEnum.DELETE,
            scope=ScopeEnum.OWN,
        )
        has_permission = self._permission_service.has_user_permission(user=user, permission_vo=delete_permission)
        if has_permission and useful_link.project.creator == user:
            return None
        else:
            logger.exception(
                f"User(id={user.id}) doesn't have enough permissions to delete ProjectUsefulLink from the Project(id={useful_link.project_id})."
            )
        raise DeleteDeniedPermissionException("You don't have enough permissions to delete this resource.")


class ProjectUsefulLinkService(UsefulLinkPermissionService):
    def __init__(
        self,
        permission_service: PermissionService,
        write_repository: ProjectUsefulLinkWriteRepository,
        read_repository: ProjectUsefulLinkReadRepository,
    ):
        super().__init__(permission_service=permission_service)
        self._write_repository = write_repository
        self._read_repository = read_repository

    def create(self, user: User, project: Project, payload: UsefulLinkCreatePayload) -> None:
        self._check_max_amount_of_links(project=project)
        self._check_create_permission(user=user, project=project)
        self._write_repository.create(data=payload)

    def _check_max_amount_of_links(self, project: Project) -> None:
        """:raises ProjectUsefulLinkMaxAmountException:"""

        links = self._read_repository.get_all(filter_=ProjectUsefulLinkFilter(project_id=Id(value=project.id)))
        if not (len(links) < USEFUL_LINKS_MAX_AMOUNT):
            raise ProjectUsefulLinkMaxAmountException(
                f"Project {project.id} already has the maximum allowed number of useful links ({USEFUL_LINKS_MAX_AMOUNT})"
            )
        return None

    def update(self, user: User, useful_link: ProjectUsefulLink, payload: UsefulLinkUpdatePayload) -> None:
        self._check_update_permission(user=user, useful_link=useful_link)
        self._write_repository.update(data=payload)

    def delete(self, user: User, useful_link: ProjectUsefulLink) -> None:
        self._check_delete_permission(user=user, useful_link=useful_link)
        self._write_repository.delete(link=useful_link)
