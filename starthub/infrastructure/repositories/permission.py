from domain.exceptions.permissions import PermissionNotFoundException
from domain.models.permission import Permission
from domain.repositories.permission import PermissionReadRepository
from domain.value_objects.common import CursorPagination, Id, OffsetPagination
from domain.value_objects.filter import PermissionFilter


class DjPermissionReadRepository(PermissionReadRepository):
    def get_by_id(self, id_: Id) -> Permission:
        permission: Permission | None = Permission.objects.filter(id=id_.value).first()
        if permission is None:
            raise PermissionNotFoundException(f"Permission with id = {id_.value} not found.")
        return permission

    def get_all(
        self, filter_: PermissionFilter, pagination: CursorPagination | OffsetPagination | None = None
    ) -> list[Permission]:
        queryset = Permission.objects.all()
        if filter_.user_id:
            queryset = queryset.filter(roles__users__id=filter_.user_id.value)
        if filter_.user:
            queryset = queryset.filter(roles__users__id=filter_.user.id)
        if filter_.role_name:
            queryset = queryset.filter(roles__name=filter_.role_name)

        return list(queryset.distinct())
