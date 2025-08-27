from abc import ABC, abstractmethod

from domain.models.project_management.project import Project
from domain.ports.repository import AbstractReadRepository, AbstractWriteRepository
from domain.value_objects.common import CursorPagination, Id, OffsetPagination, Slug
from domain.value_objects.filter import ProjectFilter
from domain.value_objects.project.project import ProjectCreatePayload, ProjectUpdatePayload


class ProjectReadRepository(AbstractReadRepository[Project, ProjectFilter, Id], ABC):
    @abstractmethod
    def get_by_id(self, id_: Id) -> Project:
        """:raises ProjectNotFoundException:"""
        pass

    @abstractmethod
    def get_all(
        self, filter_: ProjectFilter, pagination: CursorPagination | OffsetPagination | None = None
    ) -> list[Project]:
        pass

    @abstractmethod
    def get_by_slug(self, slug: Slug) -> Project:
        """:raises ProjectNotFoundException:"""
        pass


class ProjectWriteRepository(AbstractWriteRepository[Project, ProjectCreatePayload, ProjectUpdatePayload, Id], ABC):
    @abstractmethod
    def create(self, data: ProjectCreatePayload) -> Project:
        pass

    @abstractmethod
    def update(self, data: ProjectUpdatePayload) -> Project:
        """:raises ProjectNotFoundException:"""
        pass

    @abstractmethod
    def delete_by_id(self, id_: Id) -> None:
        """:raises ProjectNotFoundException:"""
        pass

    @abstractmethod
    def delete(self, project: Project) -> None:
        pass
