from typing import cast

from domain.enums.permission import ActionEnum, ScopeEnum
from domain.enums.project_status import ProjectStatusEnum
from domain.exceptions.permissions import (
    DeleteDeniedPermissionException,
    UpdateDeniedPermissionException,
    ViewDeniedPermissionException,
)
from domain.models.project_management.project import Project
from domain.models.user import User
from domain.ports.service import AbstractDomainService
from domain.repositories.project.project import ProjectWriteRepository
from domain.services.permission import PermissionService
from domain.value_objects.filter import ProjectFilter
from domain.value_objects.project.common import ProjectStatus
from domain.value_objects.project.project import ProjectCreatePayload, ProjectUpdatePayload
from domain.value_objects.user import PermissionVo
from loguru import logger


class ProjectGetService(AbstractDomainService):
    def __init__(self, permission_service: PermissionService):
        self._permission_service = permission_service

    def check_can_user_read_submissions(self, user: User) -> None:
        """:raises ViewDeniedPermissionException:"""
        view_any_submissions = self._permission_service.create_permission_vo(
            model=Project,
            action=ActionEnum.VIEW,
            scope=ScopeEnum.ANY,
            field=Project.STATUS_FIELD,
            value=ProjectStatusEnum.UNDER_MODERATION,
        )
        has_permission = self._permission_service.has_user_permission(user=user, permission_vo=view_any_submissions)
        if has_permission:
            logger.debug("User has enough permissions to view project submissions.")
            return None

        logger.error(f"User {user.email} doesn't have enough permissions to view project submissions.")
        raise ViewDeniedPermissionException("You don't have enough permissions to view project submissions.")

    def check_can_user_read_rejected(self, user: User) -> None:
        """:raises ViewDeniedPermissionException:"""
        view_any_rejected = self._permission_service.create_permission_vo(
            model=Project,
            action=ActionEnum.VIEW,
            scope=ScopeEnum.ANY,
            field=Project.STATUS_FIELD,
            value=ProjectStatusEnum.REJECTED,
        )
        has_permission = self._permission_service.has_user_permission(user=user, permission_vo=view_any_rejected)
        if has_permission:
            logger.debug("User has enough permissions to view rejected project.")
            return None

        logger.error(f"User {user.email} doesn't have enough permissions to view rejected projects.")
        raise ViewDeniedPermissionException("You don't have enough permissions to view rejected projects.")

    def check_can_user_read_cancelled(self, user: User) -> None:
        """:raises ViewDeniedPermissionException:"""
        view_any_cancelled = self._permission_service.create_permission_vo(
            model=Project,
            action=ActionEnum.VIEW,
            scope=ScopeEnum.ANY,
            field=Project.STATUS_FIELD,
            value=ProjectStatusEnum.CANCELLED,
        )
        has_permission = self._permission_service.has_user_permission(user=user, permission_vo=view_any_cancelled)
        if has_permission:
            logger.debug("User has enough permissions to view cancelled project.")
            return None

        logger.error(f"User {user.email} doesn't have enough permissions to view cancelled projects.")
        raise ViewDeniedPermissionException("You don't have enough permissions to view cancelled projects.")

    def check_can_user_read_deactivated(self, user: User) -> None:
        """:raises ViewDeniedPermissionException:"""
        view_any_cancelled = self._permission_service.create_permission_vo(
            model=Project,
            action=ActionEnum.VIEW,
            scope=ScopeEnum.ANY,
            field=Project.STATUS_FIELD,
            value=ProjectStatusEnum.DEACTIVATED,
        )
        has_permission = self._permission_service.has_user_permission(user=user, permission_vo=view_any_cancelled)
        if has_permission:
            logger.debug("User has enough permissions to view deactivated project.")
            return None

        logger.error(f"User {user.email} doesn't have enough permissions to view deactivated projects.")
        raise ViewDeniedPermissionException("You don't have enough permissions to view deactivated projects.")

    def prepare_filter_for_user(self, user: User | None, filter_: ProjectFilter) -> ProjectFilter:
        """
        Prepare a secure project filter based on user permissions.

        Validates user access to restricted project statuses and creates a filter
        that excludes projects the user is not allowed to see. If user requests
        access to restricted statuses, their permissions are validated first.

        Args:
            user: The user requesting projects (None for anonymous users)
            filter_: The original project filter with user's requirements

        Returns:
            ProjectFilter: A secure filter with appropriate exclusions applied

        Raises:
            ViewDeniedPermissionException: If user requests access to restricted
                                         content without proper permissions
        """
        self._validate_submissions_access(user, filter_)
        self._validate_rejected_access(user, filter_)
        self._validate_cancelled_access(user, filter_)
        self._validate_deactivated_access(user, filter_)

        return ProjectFilter(
            id_=filter_.id_,
            id_list=filter_.id_list,
            user_id=filter_.user_id,
            category_slug=filter_.category_slug,
            funding_model_slug=filter_.funding_model_slug,
            statuses=filter_.statuses,
            stage=filter_.stage,
            exclude_statuses=self._get_excluded_statuses(filter_=filter_),
        )

    def _get_excluded_statuses(self, filter_: ProjectFilter) -> list[ProjectStatus]:
        """
        Determine which project statuses should be excluded from results.

        Builds a list of restricted statuses that are not explicitly requested
        in the filter. This ensures users only see restricted content they
        specifically asked for (and have permissions for).

        Args:
            filter_: The project filter to analyze

        Returns:
            list[ProjectStatus]: Statuses to exclude from query results
        """
        excluded_statuses = []
        restricted_statuses = [
            ProjectStatus(value=ProjectStatusEnum.UNDER_MODERATION),
            ProjectStatus(value=ProjectStatusEnum.REJECTED),
            ProjectStatus(value=ProjectStatusEnum.CANCELLED),
            ProjectStatus(value=ProjectStatusEnum.DEACTIVATED),
        ]

        for status in restricted_statuses:
            if not filter_.statuses or status not in filter_.statuses:
                excluded_statuses.append(status)

        return excluded_statuses

    def _validate_submissions_access(self, user: User | None, filter_: ProjectFilter) -> None:
        """
        Validate user access to projects under moderation if requested.

        Args:
            user: User requesting access (None for anonymous)
            filter_: Project filter to check for submission requests

        Raises:
            ViewDeniedPermissionException: If user requests submissions without permission
        """
        if self._wants_to_see_submissions(filter_=filter_):
            if user:
                self.check_can_user_read_submissions(user=user)
            else:
                raise ViewDeniedPermissionException("You don't have enough permissions to view project submissions.")

    def _validate_rejected_access(self, user: User | None, filter_: ProjectFilter) -> None:
        if self._wants_to_see_rejected(filter_=filter_):
            if user:
                self.check_can_user_read_rejected(user=user)
            else:
                raise ViewDeniedPermissionException("You don't have enough permissions to view rejected projects.")

    def _validate_cancelled_access(self, user: User | None, filter_: ProjectFilter) -> None:
        if self._wants_to_see_cancelled(filter_=filter_):
            if user:
                self.check_can_user_read_cancelled(user=user)
            else:
                raise ViewDeniedPermissionException("You don't have enough permissions to view cancelled projects.")

    def _validate_deactivated_access(self, user: User | None, filter_: ProjectFilter) -> None:
        if self._wants_to_see_deactivated(filter_=filter_):
            if user:
                self.check_can_user_read_deactivated(user=user)
            else:
                raise ViewDeniedPermissionException("You don't have enough permissions to view deactivated projects.")

    def _build_excluded_statuses(self, filter_: ProjectFilter) -> list[ProjectStatus]:
        """
        Build list of project statuses to exclude based on filter requirements.

        This method is currently unused but provides an alternative approach
        to building exclusion lists based on what the user doesn't want to see.

        Args:
            filter_: Project filter to analyze

        Returns:
            list[ProjectStatus]: Statuses to exclude from results
        """
        excluded_statuses = []

        if not self._wants_to_see_submissions(filter_):
            excluded_statuses.append(ProjectStatus(value=ProjectStatusEnum.UNDER_MODERATION))

        if not self._wants_to_see_rejected(filter_):
            excluded_statuses.append(ProjectStatus(value=ProjectStatusEnum.REJECTED))

        if not self._wants_to_see_cancelled(filter_):
            excluded_statuses.append(ProjectStatus(value=ProjectStatusEnum.CANCELLED))

        return excluded_statuses

    def _wants_to_see_submissions(self, filter_: ProjectFilter) -> bool:
        return cast(
            bool, filter_.statuses and ProjectStatus(value=ProjectStatusEnum.UNDER_MODERATION) in filter_.statuses
        )

    def _wants_to_see_rejected(self, filter_: ProjectFilter) -> bool:
        return cast(bool, filter_.statuses and ProjectStatus(value=ProjectStatusEnum.REJECTED) in filter_.statuses)

    def _wants_to_see_cancelled(self, filter_: ProjectFilter) -> bool:
        return cast(bool, filter_.statuses and ProjectStatus(value=ProjectStatusEnum.CANCELLED) in filter_.statuses)

    def _wants_to_see_deactivated(self, filter_: ProjectFilter) -> bool:
        return cast(bool, filter_.statuses and ProjectStatus(value=ProjectStatusEnum.DEACTIVATED) in filter_.statuses)


class ProjectCreateService(AbstractDomainService):
    def __init__(
        self,
        write_repository: ProjectWriteRepository,
    ):
        self._write_repository = write_repository

    def create(self, payload: ProjectCreatePayload) -> Project:
        project: Project = self._write_repository.create(payload)
        logger.info("Project created successfully.")
        return project


class ProjectUpdateService(AbstractDomainService):
    def __init__(
        self,
        write_repository: ProjectWriteRepository,
        permission_service: PermissionService,
    ):
        self._write_repository = write_repository
        self._permission_service = permission_service

    def update(self, project: Project, user: User, update_payload: ProjectUpdatePayload) -> None:
        self._check_update_permission(user=user, project=project)
        self._write_repository.update(data=update_payload)

    def _check_update_permission(self, user: User, project: Project) -> None:
        if self._has_update_any_permission(user=user):
            return

        change_own_permission: PermissionVo = self._permission_service.create_permission_vo(
            model=Project, action=ActionEnum.CHANGE, scope=ScopeEnum.OWN
        )
        has_permission: bool = self._permission_service.has_user_permission(
            user=user, permission_vo=change_own_permission
        )
        if has_permission:
            if project.creator == user:
                return

        logger.exception(f"User {user} does not have enough permissions to update the project {project}.")
        raise UpdateDeniedPermissionException("You don't have enough permissions to update this project.")

    def _has_update_any_permission(self, user: User) -> bool:
        change_any_permission: PermissionVo = self._permission_service.create_permission_vo(
            model=Project, action=ActionEnum.CHANGE, scope=ScopeEnum.ANY
        )
        has_permission: bool = self._permission_service.has_user_permission(
            user=user, permission_vo=change_any_permission
        )
        return has_permission


class ProjectDeleteService(AbstractDomainService):
    def __init__(
        self,
        write_repository: ProjectWriteRepository,
        permission_service: PermissionService,
    ):
        self._write_repository = write_repository
        self._permission_service = permission_service

    def delete(self, project: Project, user: User) -> None:
        """:raises DeleteDeniedPermissionException:"""

        self._check_delete_permission(project=project, user=user)
        self._write_repository.delete(project=project)

        logger.info("Project deleted successfully.")

    def _check_delete_permission(self, user: User, project: Project) -> None:
        if self._has_delete_any_permission(user=user):
            return

        delete_own_permission: PermissionVo = self._permission_service.create_permission_vo(
            model=Project, action=ActionEnum.DELETE, scope=ScopeEnum.OWN
        )
        has_own_permission: bool = self._permission_service.has_user_permission(
            user=user, permission_vo=delete_own_permission
        )
        if has_own_permission:
            if project.creator == user:
                return

        logger.exception(f"User: {user} does not have enogh permissions to delete the project: {project}")
        raise DeleteDeniedPermissionException("You don't have enough permissions to delete this project.")

    def _has_delete_any_permission(self, user: User) -> bool:
        delete_any_permission: PermissionVo = self._permission_service.create_permission_vo(
            model=Project, action=ActionEnum.DELETE, scope=ScopeEnum.ANY
        )
        has_any_permission: bool = self._permission_service.has_user_permission(
            user=user, permission_vo=delete_any_permission
        )
        return has_any_permission


class ProjectService(ProjectGetService, ProjectCreateService, ProjectUpdateService, ProjectDeleteService):
    def __init__(self, write_repository: ProjectWriteRepository, permission_service: PermissionService):
        ProjectGetService.__init__(self, permission_service)
        ProjectCreateService.__init__(self, write_repository)
        ProjectUpdateService.__init__(self, write_repository, permission_service)
        ProjectDeleteService.__init__(self, write_repository, permission_service)
