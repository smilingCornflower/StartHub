from domain.exceptions.project_management import ProjectInvestmentNotFoundException
from domain.models.project_management.investment import ProjectInvestment, ProjectInvestmentSocialLink
from domain.repositories.project.investment import (
    ProjectInestmentReadRepository,
    ProjectInvestmentWriteRepository,
    ProjectInvestmentSocialLinkReadRepository, ProjectInvestmentSocialLinkWriteRepository,
)
from domain.value_objects.common import Pagination
from domain.value_objects.filter import ProjectInvestmentFilter, ProjectInvestmentSocialLinkFilter
from domain.value_objects.project.investment import (
    ProjectInvestmentCreatePayload,
    ProjectInvestmentId,
    ProjectInvestmentUpdatePayload,
)
from domain.value_objects.project.project_investment_social_link import ProjectInvestmentSocialLinkId, \
    ProjectInvestmentSocialLinkUpdatePayload, ProjectInvestmentSocialLinkCreatePayload
from infrastructure.repositories.pagination import apply_pagination


class DjProjectInvestmentReadRepository(ProjectInestmentReadRepository):
    def get_by_id(self, id_: ProjectInvestmentId) -> ProjectInvestment:
        """:raises ProjectInvestmentNotFoundException:"""
        investment: ProjectInvestment | None = ProjectInvestment.objects.filter(id=id_.value).first()
        if investment is None:
            raise ProjectInvestmentNotFoundException(f"ProjectInvestment with id = {id_.value} not found.")
        return investment

    def get_all(
        self, filter_: ProjectInvestmentFilter, pagination: Pagination | None = None
    ) -> list[ProjectInvestment]:
        queryset = ProjectInvestment.objects.all()
        if filter_.project_id is not None:
            queryset = queryset.filter(project_id=filter_.project_id.value)

        if pagination is not None:
            return apply_pagination(queryset=queryset, pagination=pagination)

        return list(queryset)


class DjProjectInvestmentWriteRepository(ProjectInvestmentWriteRepository):
    def create(self, data: ProjectInvestmentCreatePayload) -> ProjectInvestment:
        return ProjectInvestment.objects.create(
            project_id=data.project_id.value,
            organization_name=data.organization_name.value,
            amount=data.amount.value,
        )

    def update(self, data: ProjectInvestmentUpdatePayload) -> ProjectInvestment:
        raise NotImplementedError("The method update() is not implemented yet.")

    def delete_by_id(self, id_: ProjectInvestmentId) -> None:
        raise NotImplementedError("The method delete_by_id() is not implemented yet.")


# ======================================================================================================================


class DjProjectInvestmentSocialLinkReadRepository(ProjectInvestmentSocialLinkReadRepository):
    def get_by_id(self, id_: ProjectInvestmentSocialLinkId) -> ProjectInvestmentSocialLink:
        raise NotImplementedError("The method get_by_id() is not implemented yet.")

    def get_all(
        self, filter_: ProjectInvestmentSocialLinkFilter, pagination: Pagination | None = None
    ) -> list[ProjectInvestmentSocialLink]:
        raise NotImplementedError("The method  list() is not implemented yet.")


class DjProjectInvestmentSocialLinkWriteRepository(ProjectInvestmentSocialLinkWriteRepository):
    def create(self, data: ProjectInvestmentSocialLinkCreatePayload) -> ProjectInvestmentSocialLink:
        raise NotImplementedError("The method create() is not implemented yet.")

    def update(self, data: ProjectInvestmentSocialLinkUpdatePayload) -> ProjectInvestmentSocialLink:
        raise NotImplementedError("The method update() is not implemented yet.")

    def delete_by_id(self, id_: ProjectInvestmentSocialLinkId) -> None:
        raise NotImplementedError("The method delete_by_id() is not implemented yet.")