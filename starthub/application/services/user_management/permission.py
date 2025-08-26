from application.dto.permission import PermissionDto
from application.ports.service import AbstractAppService
from domain.enums.permission import ActionEnum, ScopeEnum
from domain.enums.role import RoleEnum
from domain.exceptions.permissions import ViewDeniedPermissionException
from domain.models.permission import Permission
from domain.models.user_management.user import User
from domain.repositories.permission import PermissionReadRepository
from domain.repositories.user_management.user import UserReadRepository
from domain.services.permission import PermissionService
from domain.value_objects.common import Id
from domain.value_objects.filter import PermissionFilter


class PermissionAppService(AbstractAppService):
    def __init__(
        self,
        permission_service: PermissionService,
        permission_read_reposiotory: PermissionReadRepository,
        user_read_repository: UserReadRepository,
    ):
        self._permission_service = permission_service
        self._permission_read_repository = permission_read_reposiotory
        self._user_read_repository = user_read_repository

    def get(self, user_id: Id, role_name: RoleEnum | None) -> list[PermissionDto]:
        user = self._user_read_repository.get_by_id(id_=user_id)
        self._check_can_user_view_any_permissions(user=user)
        permissions = self._permission_read_repository.get_all(filter_=PermissionFilter(role_name=role_name))
        return [PermissionDto(id=i.id, name=i.name) for i in permissions]

    def _check_can_user_view_any_permissions(self, user: User) -> None:
        """
        Checks that can user view permission values
        :raises ViewDeniedPermissionException:
        """
        if self._permission_service.is_allowed_for_user(
            user=user,
            model=Permission,
            action=ActionEnum.VIEW,
            scope=ScopeEnum.ANY,
        ):
            return None
        else:
            raise ViewDeniedPermissionException("You don't have enough permissions to view permission values.")
