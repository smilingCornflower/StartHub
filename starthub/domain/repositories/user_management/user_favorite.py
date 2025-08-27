from abc import ABC, abstractmethod

from domain.models.user_management.user_favorite import UserFavorite
from domain.ports.repository import AbstractReadRepository, AbstractWriteRepository
from domain.value_objects.common import CursorPagination, Id, OffsetPagination
from domain.value_objects.filter import UserFavoriteFilter
from domain.value_objects.user_management.user_favorite import UserFavoriteCreatePayload, UserFavoriteUpdatePayload


class UserFavoriteReadRepository(AbstractReadRepository[UserFavorite, UserFavoriteFilter, Id], ABC):
    @abstractmethod
    def get_by_id(self, id_: Id) -> UserFavorite:
        """:raises UserFavoriteNotFoundException:"""

    @abstractmethod
    def get_all(
        self, filter_: UserFavoriteFilter, pagination: CursorPagination | OffsetPagination | None = None
    ) -> list[UserFavorite]:
        pass

    @abstractmethod
    def get_by_association_ids(self, user_id: Id, project_id: Id) -> UserFavorite:
        """:raises UserFavoriteNotFoundException:"""
        pass


class UserFavoriteWriteRepository(
    AbstractWriteRepository[UserFavorite, UserFavoriteCreatePayload, UserFavoriteUpdatePayload, Id], ABC
):
    @abstractmethod
    def create(self, data: UserFavoriteCreatePayload) -> UserFavorite:
        pass

    @abstractmethod
    def update(self, data: UserFavoriteUpdatePayload) -> UserFavorite:
        pass

    @abstractmethod
    def delete_by_id(self, id_: Id) -> None:
        pass

    @abstractmethod
    def delete_by_association_ids(self, user_id: Id, project_id: Id) -> None:
        pass
