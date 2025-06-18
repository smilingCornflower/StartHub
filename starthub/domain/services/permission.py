from domain.enums.permission import ActionEnum, ScopeEnum
from domain.models.base import BaseModel
from domain.models.permission import Permission
from domain.ports.service import AbstractDomainService
from domain.repositories.permission import PermissionReadRepository
from domain.repositories.user import UserReadRepository
from domain.value_objects.common import Id
from domain.value_objects.filter import PermissionFilter
from domain.value_objects.user import PermissionVo
from loguru import logger


class PermissionService(AbstractDomainService):
    def __init__(
        self,
        user_read_repository: UserReadRepository,
        permission_read_repository: PermissionReadRepository,
    ):
        self._user_read_repository = user_read_repository
        self._permission_read_repository = permission_read_repository

    def has_permission(self, user_id: Id, permission_vo: PermissionVo) -> bool:
        """
        :raises UserNotFoundException:
        """
        self._user_read_repository.get_by_id(id_=user_id)  # check
        permissions: list[Permission] = self._permission_read_repository.get_all(PermissionFilter(user_id=user_id))
        permission_names = {p.name for p in permissions}
        logger.debug(f"user_id: {user_id.value}, permissions: {permission_names}")
        return permission_vo.value in permission_names

    @classmethod
    def create_permission_vo(
        cls, model: type[BaseModel], action: ActionEnum, scope: ScopeEnum, field: str | None = None
    ) -> PermissionVo:
        """
        :raises TypeError:
        :raises ValueError:
        """
        if not issubclass(model, BaseModel):
            raise TypeError("Model must inherit from BaseModel.")
        if field:
            if hasattr(model, field):
                permission_value = f"{action}.{scope}.{model.get_permission_key()}.{field}"
            else:
                raise ValueError(f"Field '{field}' does not exist in model '{model.__name__}'")
        else:
            permission_value = f"{action}.{scope}.{model.get_permission_key()}"

        logger.debug(f"{permission_value=}")
        return PermissionVo(value=permission_value)
