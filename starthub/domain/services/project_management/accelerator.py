from domain.enums.permission import ActionEnum, ScopeEnum
from domain.exceptions.permissions import DeleteDeniedPermissionException
from domain.models.project_management.accelerator import ProjectAccelerator
from domain.models.user import User
from domain.ports.service import AbstractDomainService
from domain.repositories.project.accelerator import ProjectAcceleratorWriteRepository
from domain.services.permission import PermissionService
from domain.value_objects.project.accelerator import ProjectAcceleratorCreatePayload, ProjectAcceleratorUpdatePayload
from loguru import logger


class ProjectAcceleratorService(AbstractDomainService):
    def __init__(self, write_repository: ProjectAcceleratorWriteRepository, permission_service: PermissionService):
        self._write_repository = write_repository
        self._permission_service = permission_service

    def create(self, payload: ProjectAcceleratorCreatePayload) -> ProjectAccelerator:
        return self._write_repository.create(data=payload)

    def update(self, payload: ProjectAcceleratorUpdatePayload) -> ProjectAccelerator:
        return self._write_repository.update(data=payload)

    def delete(self, user: User, accelerator: ProjectAccelerator) -> None:
        self._check_delete_permissions(user=user, accelerator=accelerator)
        self._write_repository.delete(accelerator=accelerator)

    def _check_delete_permissions(self, user: User, accelerator: ProjectAccelerator) -> None:
        """:raises DeleteDeniedPermissionException:"""
        delete_own_permission = self._permission_service.create_permission_vo(
            model=ProjectAccelerator, action=ActionEnum.DELETE, scope=ScopeEnum.OWN
        )
        has_permission = self._permission_service.has_user_permission(user=user, permission_vo=delete_own_permission)
        if has_permission:
            if accelerator.project.creator == user:
                return None

        logger.exception(
            f"User with id = {user.id} doesn't have have enough permissions to delete the accelerator with id = {accelerator.id}."
        )
        raise DeleteDeniedPermissionException("You don't have enough permissions to delete this resource.")
