from abc import ABC, abstractmethod

from domain.models.project import Project
from domain.ports.repository import AbstractReadRepository, AbstractWriteRepository
from domain.value_objects.common import Id, Slug
from domain.value_objects.filter import ProjectFilter
from domain.value_objects.project import ProjectCreatePayload, ProjectUpdatePayload


class ProjectReadRepository(AbstractReadRepository[Project, ProjectFilter], ABC):
    @abstractmethod
    def get_by_id(self, id_: Id) -> Project:
        """:raises ProjectNotFoundException:"""
        pass

    @abstractmethod
    def get_all(self, filter_: ProjectFilter) -> list[Project]:
        pass

    @abstractmethod
    def get_by_slug(self, slug: Slug) -> Project:
        """:raises ProjectNotFoundException:"""
        pass


class ProjectWriteRepository(AbstractWriteRepository[Project, ProjectCreatePayload, ProjectUpdatePayload], ABC):
    @abstractmethod
    def create(self, data: ProjectCreatePayload) -> Project:
        pass

    @abstractmethod
    def update(self, data: ProjectUpdatePayload) -> Project:
        """:raises ProjectNotFoundException:"""
        pass

    @abstractmethod
    def delete(self, id_: Id) -> None:
        """:raises ProjectNotFoundException:"""
        pass
