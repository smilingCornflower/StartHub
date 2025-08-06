from abc import ABC, abstractmethod

from domain.models.project_management.image import ProjectImage
from domain.ports.repository import AbstractReadRepository, AbstractWriteRepository
from domain.value_objects.common import Id, Pagination
from domain.value_objects.filter import ProjectImageFilter
from domain.value_objects.project.image import (
    ProjectImageCreatePayload,
    ProjectImageDeletePayload,
    ProjectImageUpdatePayload,
)


class ProjectImageReadRepository(AbstractReadRepository[ProjectImage, ProjectImageFilter, Id], ABC):
    @abstractmethod
    def get_by_id(self, id_: Id) -> ProjectImage:
        """:raises ProjectPhotoNotFoundException:"""
        pass

    @abstractmethod
    def get_all(self, filter_: ProjectImageFilter, pagination: Pagination | None = None) -> list[ProjectImage]:
        pass


class ProjectImageWriteRepository(
    AbstractWriteRepository[ProjectImage, ProjectImageCreatePayload, ProjectImageUpdatePayload, Id], ABC
):
    @abstractmethod
    def create(self, data: ProjectImageCreatePayload) -> ProjectImage:
        pass

    @abstractmethod
    def update(self, data: ProjectImageUpdatePayload) -> ProjectImage:
        pass

    @abstractmethod
    def delete_by_id(self, id_: Id) -> None:
        pass

    @abstractmethod
    def delete(self, data: ProjectImageDeletePayload) -> None:
        pass
