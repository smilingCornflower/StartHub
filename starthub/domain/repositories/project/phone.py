from abc import ABC, abstractmethod

from domain.models.project_management.phone import ProjectPhone
from domain.ports.repository import AbstractReadRepository, AbstractWriteRepository
from domain.value_objects.common import Id, Pagination
from domain.value_objects.filter import ProjectPhoneFilter
from domain.value_objects.project.phone import ProjectPhoneCreatePayload, ProjectPhoneUpdatePayload


class ProjectPhoneReadRepository(AbstractReadRepository[ProjectPhone, ProjectPhoneFilter, Id], ABC):
    @abstractmethod
    def get_by_id(self, id_: Id) -> ProjectPhone:
        pass

    @abstractmethod
    def get_all(self, filter_: ProjectPhoneFilter, pagination: Pagination | None = None) -> list[ProjectPhone]:
        pass


class ProjectPhoneWriteRepository(
    AbstractWriteRepository[ProjectPhone, ProjectPhoneCreatePayload, ProjectPhoneUpdatePayload, Id], ABC
):
    @abstractmethod
    def create(self, data: ProjectPhoneCreatePayload) -> ProjectPhone:
        pass

    @abstractmethod
    def update(self, data: ProjectPhoneUpdatePayload) -> ProjectPhone:
        pass

    @abstractmethod
    def delete_by_id(self, id_: Id) -> None:
        pass
