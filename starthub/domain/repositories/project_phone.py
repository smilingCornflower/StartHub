from abc import ABC, abstractmethod

from domain.models.project import ProjectPhone
from domain.ports.repository import AbstractReadRepository, AbstractWriteRepository
from domain.value_objects.common import Id
from domain.value_objects.filter import ProjectPhoneFilter
from domain.value_objects.project_phone import ProjectPhoneCreatePayload, ProjectPhoneUpdatePayload


class ProjectPhoneReadRepository(AbstractReadRepository[ProjectPhone, ProjectPhoneFilter], ABC):
    @abstractmethod
    def get_by_id(self, id_: Id) -> ProjectPhone:
        pass

    @abstractmethod
    def get_all(self, filter_: ProjectPhoneFilter) -> list[ProjectPhone]:
        pass


class ProjectPhoneWriteRepository(
    AbstractWriteRepository[ProjectPhone, ProjectPhoneCreatePayload, ProjectPhoneUpdatePayload], ABC
):
    @abstractmethod
    def create(self, data: ProjectPhoneCreatePayload) -> ProjectPhone:
        pass

    @abstractmethod
    def update(self, data: ProjectPhoneUpdatePayload) -> ProjectPhone:
        pass

    @abstractmethod
    def delete(self, id_: Id) -> None:
        pass
