from abc import ABC, abstractmethod

from domain.models.permission import Permission
from domain.ports.repository import AbstractReadRepository
from domain.value_objects.common import CursorPagination, Id, OffsetPagination
from domain.value_objects.filter import PermissionFilter


class PermissionReadRepository(AbstractReadRepository[Permission, PermissionFilter, Id], ABC):
    @abstractmethod
    def get_by_id(self, id_: Id) -> Permission:
        """:raises PermissionNotFoundException:"""
        pass

    @abstractmethod
    def get_all(
        self, filter_: PermissionFilter, pagination: CursorPagination | OffsetPagination | None = None
    ) -> list[Permission]:
        pass
