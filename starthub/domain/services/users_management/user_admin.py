from domain.enums.permission import ActionEnum, ScopeEnum
from domain.exceptions.permissions import (
    AddDeniedPermissionException,
    UpdateDeniedPermissionException,
    ViewDeniedPermissionException,
)
from domain.models.role import Role
from domain.models.user_management.user import User
from domain.ports.service import AbstractDomainService
from domain.repositories.user_management.user import UserWriteRepository
from domain.services.permission import PermissionService
from domain.value_objects.common import Id
from domain.value_objects.user_management.user import UserUpdatePayload
from loguru import logger


class UserAdminPermissionService(AbstractDomainService):
    def __init__(self, permission_service: PermissionService):
        self._permission_service = permission_service

    def _check_permission_to_add_user_role(self, user: User, role: Role) -> None:
        """:raises AddDeniedPermissionException:"""
        if self._permission_service.is_allowed_for_user(
            user=user, model=User, action=ActionEnum.ADD, scope=ScopeEnum.ANY, field=User.ROLES_FIELD, value=role.name
        ):
            return None
        else:
            logger.error(f"User {user.email} has no permission to add role '{role}'.")
            raise AddDeniedPermissionException(f"You don't have enough permissions to add role '{role}'.")

    def _check_permission_to_remove_user_role(self, user: User, role: Role) -> None:
        """:raises AddDeniedPermissionException:"""
        if self._permission_service.is_allowed_for_user(
            user=user, model=User, action=ActionEnum.ADD, scope=ScopeEnum.ANY, field=User.ROLES_FIELD, value=role.name
        ):
            return None
        else:
            logger.error(f"User {user.email} has no permission to add role '{role}'.")
            raise AddDeniedPermissionException(f"You don't have enough permissions to add role '{role}'.")

    def _check_permission_to_change_is_active_field(self, user: User) -> None:
        if self._permission_service.is_allowed_for_user(
            user=user, model=User, action=ActionEnum.CHANGE, scope=ScopeEnum.ANY, field=User.IS_ACTIVE_FIELD
        ):
            return None
        else:
            logger.error(f"User {user.email} has no permission to change is_active field for users.")
            raise UpdateDeniedPermissionException(
                "You don't have enough permissions to change is_active field for users."
            )

    def check_permission_to_view_any_user_details(self, user: User) -> None:
        """:raises ViewDeniedPermissionException:"""
        if self._permission_service.is_allowed_for_user(
            user=user,
            model=User,
            action=ActionEnum.VIEW,
            scope=ScopeEnum.ANY,
            field=User.DETAILS_FIED,
        ):
            return None
        else:
            logger.error(f"User {user.email} has no permission to view user details.")
            raise ViewDeniedPermissionException("You don't have enough permissions to view user details.")


class UserAdminService(UserAdminPermissionService):
    def __init__(self, permission_service: PermissionService, user_write_repository: UserWriteRepository):
        super().__init__(permission_service=permission_service)
        self._user_write_repository = user_write_repository

    def add_role_to_user(self, caller_user: User, target_user: User, role: Role) -> None:
        self._check_permission_to_add_user_role(user=caller_user, role=role)
        update_payload = UserUpdatePayload(id_=Id(value=target_user.id), role_to_add=role)
        self._user_write_repository.update(data=update_payload)
        logger.info("User role added successfully.")

    def remove_role_form_user(self, caller_user: User, target_user: User, role: Role) -> None:
        self._check_permission_to_remove_user_role(user=caller_user, role=role)
        update_payload = UserUpdatePayload(id_=Id(value=target_user.id), role_to_remove=role)
        self._user_write_repository.update(data=update_payload)
        logger.info("User role removed successfully.")

    def activate(self, caller_user: User, target_user: User) -> None:
        self._check_permission_to_change_is_active_field(user=caller_user)
        update_payload = UserUpdatePayload(id_=Id(value=target_user.id), is_active=True)
        self._user_write_repository.update(data=update_payload)
        logger.info("User activated successfully.")

    def deactivate(self, caller_user: User, target_user: User) -> None:
        self._check_permission_to_change_is_active_field(user=caller_user)
        update_payload = UserUpdatePayload(id_=Id(value=target_user.id), is_active=False)
        self._user_write_repository.update(data=update_payload)
        logger.info("User deactivated successfully.")
