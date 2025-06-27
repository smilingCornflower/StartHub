from domain.models.role import Role
from domain.repositories.role import RoleReadRepository
from domain.value_objects.common import Id, Pagination
from domain.value_objects.filter import RoleFilter


class DjRoleReadRepository(RoleReadRepository):
    def get_by_id(self, id_: Id) -> Role:
        raise NotImplementedError("get_by_id() is not implemented yet.")

    def get_all(self, filter_: RoleFilter, pagination: Pagination | None = None) -> list[Role]:
        queryset = Role.objects.all()
        return list(queryset.distinct())
