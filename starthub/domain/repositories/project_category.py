from abc import ABC, abstractmethod

from domain.models.project_category import ProjectCategory
from domain.ports.repository import AbstractReadRepository, AbstractWriteRepository
from domain.value_objects.common import Id
from domain.value_objects.filter import ProjectCategoryFilter
from domain.value_objects.project_category import ProjectCategoryCreatePayload, ProjectCategoryUpdatePayload


class ProjectCategoryReadRepository(AbstractReadRepository[ProjectCategory, ProjectCategoryFilter], ABC):
    @abstractmethod
    def get_by_id(self, id_: Id) -> ProjectCategory:
        """:raises ProjectCategoryNotFoundException:"""
        pass

    @abstractmethod
    def get_all(self, filter_: ProjectCategoryFilter) -> list[ProjectCategory]:
        pass


class ProjectCategoryWriteRepository(
    AbstractWriteRepository[ProjectCategory, ProjectCategoryCreatePayload, ProjectCategoryUpdatePayload], ABC
):
    @abstractmethod
    def create(self, data: ProjectCategoryCreatePayload) -> ProjectCategory:
        pass

    @abstractmethod
    def update(self, data: ProjectCategoryUpdatePayload) -> ProjectCategory:
        """:raises ProjectCategoryNotFoundException:"""
        pass

    @abstractmethod
    def delete(self, id_: Id) -> None:
        """:raises ProjectCategoryNotFoundException:"""
        pass
