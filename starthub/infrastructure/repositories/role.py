from domain.enums.role import RoleEnum
from domain.exceptions.role import RoleNotFoundException
from domain.models.role import Role
from domain.repositories.role import RoleReadRepository
from domain.value_objects.common import CursorPagination, Id, OffsetPagination
from domain.value_objects.filter import RoleFilter
from loguru import logger


class DjRoleReadRepository(RoleReadRepository):
    def get_by_id(self, id_: Id) -> Role:
        raise NotImplementedError("get_by_id() is not implemented yet.")

    def get_all(self, filter_: RoleFilter, pagination: CursorPagination | OffsetPagination | None = None) -> list[Role]:
        queryset = Role.objects.all()
        if filter_.user_id:
            queryset = queryset.filter(users__id=filter_.user_id.value)

        return list(queryset.distinct())

    def get_by_name(self, name: RoleEnum) -> Role:
        """:raises RoleNotFoundException:"""
        try:
            return Role.objects.get(name=name)
        except Role.DoesNotExist:
            logger.exception(f"Role with name = {name} does not found.")
            raise RoleNotFoundException(f"Role with name = {name} does not found.")
