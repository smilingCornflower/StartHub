from abc import ABC, abstractmethod

from domain.models.project_management.category import ProjectCategory
from domain.ports.repository import AbstractReadRepository, AbstractWriteRepository
from domain.value_objects.common import CursorPagination, Id, OffsetPagination
from domain.value_objects.filter import ProjectCategoryFilter
from domain.value_objects.project.category import ProjectCategoryCreatePayload, ProjectCategoryUpdatePayload


class ProjectCategoryReadRepository(AbstractReadRepository[ProjectCategory, ProjectCategoryFilter, Id], ABC):
    @abstractmethod
    def get_by_id(self, id_: Id) -> ProjectCategory:
        """:raises ProjectCategoryNotFoundException:"""
        pass

    @abstractmethod
    def get_all(
        self, filter_: ProjectCategoryFilter, pagination: CursorPagination | OffsetPagination | None = None
    ) -> list[ProjectCategory]:
        pass


class ProjectCategoryWriteRepository(
    AbstractWriteRepository[ProjectCategory, ProjectCategoryCreatePayload, ProjectCategoryUpdatePayload, Id], ABC
):
    @abstractmethod
    def create(self, data: ProjectCategoryCreatePayload) -> ProjectCategory:
        pass

    @abstractmethod
    def update(self, data: ProjectCategoryUpdatePayload) -> ProjectCategory:
        """:raises ProjectCategoryNotFoundException:"""
        pass

    @abstractmethod
    def delete_by_id(self, id_: Id) -> None:
        """:raises ProjectCategoryNotFoundException:"""
        pass
