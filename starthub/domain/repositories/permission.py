from abc import ABC, abstractmethod

from domain.models.permission import Permission
from domain.ports.repository import AbstractReadRepository
from domain.value_objects.common import Id
from domain.value_objects.filter import PermissionFilter


class PermissionReadRepository(AbstractReadRepository[Permission, PermissionFilter], ABC):
    @abstractmethod
    def get_by_id(self, id_: Id) -> Permission:
        """:raises PermissionNotFoundException:"""
        pass

    @abstractmethod
    def get_all(self, filter_: PermissionFilter) -> list[Permission]:
        pass
