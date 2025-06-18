from abc import ABC, abstractmethod

from domain.models.role import Role
from domain.ports.repository import AbstractReadRepository
from domain.value_objects.common import Id
from domain.value_objects.filter import RoleFilter


class RoleReadRepository(AbstractReadRepository[Role, RoleFilter], ABC):
    @abstractmethod
    def get_by_id(self, id_: Id) -> Role:
        """:raises PermissionNotFoundException:"""
        pass

    @abstractmethod
    def get_all(self, filter_: RoleFilter) -> list[Role]:
        pass
