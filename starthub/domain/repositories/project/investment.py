from abc import ABC, abstractmethod

from domain.models import ProjectInvestmentPhone
from domain.models.project_management.investment import ProjectInvestment, ProjectInvestmentSocialLink
from domain.ports.repository import AbstractReadRepository, AbstractWriteRepository
from domain.value_objects.common import Pagination
from domain.value_objects.filter import (
    ProjectInvestmentFilter,
    ProjectInvestmentPhoneFilter,
    ProjectInvestmentSocialLinkFilter,
)
from domain.value_objects.project.investment import (
    ProjectInvestmentCreatePayload,
    ProjectInvestmentId,
    ProjectInvestmentUpdatePayload,
)
from domain.value_objects.project.project_investment_phone import (
    ProjectInvestmentPhoneCreatePayload,
    ProjectInvestmentPhoneUpdatePayload,
)
from domain.value_objects.project.project_investment_social_link import (
    ProjectInvestmentSocialLinkCreatePayload,
    ProjectInvestmentSocialLinkId,
    ProjectInvestmentSocialLinkUpdatePayload,
)


class ProjectInvestmentReadRepository(
    AbstractReadRepository[ProjectInvestment, ProjectInvestmentFilter, ProjectInvestmentId], ABC
):
    @abstractmethod
    def get_by_id(self, id_: ProjectInvestmentId) -> ProjectInvestment:
        pass

    @abstractmethod
    def get_all(
        self, filter_: ProjectInvestmentFilter, pagination: Pagination | None = None
    ) -> list[ProjectInvestment]:
        pass


class ProjectInvestmentWriteRepository(
    AbstractWriteRepository[
        ProjectInvestment, ProjectInvestmentCreatePayload, ProjectInvestmentUpdatePayload, ProjectInvestmentId
    ],
    ABC,
):
    @abstractmethod
    def create(self, data: ProjectInvestmentCreatePayload) -> ProjectInvestment:
        pass

    @abstractmethod
    def update(self, data: ProjectInvestmentUpdatePayload) -> ProjectInvestment:
        pass

    @abstractmethod
    def delete_by_id(self, id_: ProjectInvestmentId) -> None:
        pass


# ======================================================================================================================
class ProjectInvestmentSocialLinkReadRepository(
    AbstractReadRepository[
        ProjectInvestmentSocialLink, ProjectInvestmentSocialLinkFilter, ProjectInvestmentSocialLinkId
    ],
    ABC,
):
    @abstractmethod
    def get_by_id(self, id_: ProjectInvestmentSocialLinkId) -> ProjectInvestmentSocialLink:
        pass

    @abstractmethod
    def get_all(
        self, filter_: ProjectInvestmentSocialLinkFilter, pagination: Pagination | None = None
    ) -> list[ProjectInvestmentSocialLink]:
        pass


class ProjectInvestmentSocialLinkWriteRepository(
    AbstractWriteRepository[
        ProjectInvestmentSocialLink,
        ProjectInvestmentSocialLinkCreatePayload,
        ProjectInvestmentSocialLinkUpdatePayload,
        ProjectInvestmentSocialLinkId,
    ],
    ABC,
):
    @abstractmethod
    def create(self, data: ProjectInvestmentSocialLinkCreatePayload) -> ProjectInvestmentSocialLink:
        pass

    @abstractmethod
    def update(self, data: ProjectInvestmentSocialLinkUpdatePayload) -> ProjectInvestmentSocialLink:
        pass

    @abstractmethod
    def delete_by_id(self, id_: ProjectInvestmentSocialLinkId) -> None:
        pass

    @abstractmethod
    def delete(self, investment: ProjectInvestmentSocialLink) -> None:
        pass


class ProjectInvestmentPhoneReadRepository(
    AbstractReadRepository[ProjectInvestmentPhone, ProjectInvestmentPhoneFilter, ProjectInvestmentId], ABC
):
    @abstractmethod
    def get_by_id(self, id_: ProjectInvestmentId) -> ProjectInvestment:
        pass

    @abstractmethod
    def get_all(
        self, filter_: ProjectInvestmentPhoneFilter, pagination: Pagination | None = None
    ) -> list[ProjectInvestmentPhone]:
        pass


class ProjectInvestmentPhoneWriteRepository(
    AbstractWriteRepository[
        ProjectInvestmentPhone,
        ProjectInvestmentPhoneCreatePayload,
        ProjectInvestmentPhoneUpdatePayload,
        ProjectInvestmentId,
    ],
    ABC,
):
    @abstractmethod
    def create(self, data: ProjectInvestmentPhoneCreatePayload) -> ProjectInvestmentPhone:
        pass

    @abstractmethod
    def update(self, data: ProjectInvestmentPhoneUpdatePayload) -> ProjectInvestmentPhone:
        pass

    @abstractmethod
    def delete_by_id(self, id_: ProjectInvestmentId) -> None:
        pass
