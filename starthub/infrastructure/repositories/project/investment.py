from domain.exceptions.project_management import ProjectInvestmentNotFoundException
from domain.models.project_management.investment import (
    ProjectInvestment,
    ProjectInvestmentPhone,
    ProjectInvestmentSocialLink,
)
from domain.repositories.project.investment import (
    ProjectInvestmentPhoneReadRepository,
    ProjectInvestmentPhoneWriteRepository,
    ProjectInvestmentReadRepository,
    ProjectInvestmentSocialLinkReadRepository,
    ProjectInvestmentSocialLinkWriteRepository,
    ProjectInvestmentWriteRepository,
)
from domain.value_objects.common import CursorPagination, OffsetPagination
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
from infrastructure.repositories.pagination import apply_pagination


class DjProjectInvestmentReadRepository(ProjectInvestmentReadRepository):
    def get_by_id(self, id_: ProjectInvestmentId) -> ProjectInvestment:
        """:raises ProjectInvestmentNotFoundException:"""
        investment: ProjectInvestment | None = ProjectInvestment.objects.filter(id=id_.value).first()
        if investment is None:
            raise ProjectInvestmentNotFoundException(f"ProjectInvestment with id = {id_.value} not found.")
        return investment

    def get_all(
        self, filter_: ProjectInvestmentFilter, pagination: CursorPagination | OffsetPagination | None = None
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
        """:raises ProjectInvestmentNotFoundException:"""
        investment: ProjectInvestment | None = ProjectInvestment.objects.filter(id=data.investment_id.value).first()

        if investment is None:
            raise ProjectInvestmentNotFoundException(
                f"Project investment with id = {data.investment_id.value} does not exist."
            )

        if data.organization_name is not None:
            investment.organization_name = data.organization_name.value
            investment.slug = None

        if data.amount is not None:
            investment.amount = data.amount.value

        investment.save()
        return investment

    def delete_by_id(self, id_: ProjectInvestmentId) -> None:
        raise NotImplementedError("The method delete_by_id() is not implemented yet.")


# ======================================================================================================================


class DjProjectInvestmentSocialLinkReadRepository(ProjectInvestmentSocialLinkReadRepository):
    def get_by_id(self, id_: ProjectInvestmentSocialLinkId) -> ProjectInvestmentSocialLink:
        """:raises ProjectInvestmentNotFoundException:"""
        investment: ProjectInvestmentSocialLink | None = ProjectInvestmentSocialLink.objects.filter(
            id=id_.value
        ).first()
        if investment is None:
            raise ProjectInvestmentNotFoundException(f"Project investment with id = {id_.value} not found.")
        return investment

    def get_all(
        self, filter_: ProjectInvestmentSocialLinkFilter, pagination: CursorPagination | OffsetPagination | None = None
    ) -> list[ProjectInvestmentSocialLink]:
        queryset = ProjectInvestmentSocialLink.objects.all()

        if filter_.investment_id is not None:
            queryset = queryset.filter(investment_id=filter_.investment_id.value)

        if pagination:
            return apply_pagination(queryset=queryset, pagination=pagination)

        return list(queryset)


class DjProjectInvestmentSocialLinkWriteRepository(ProjectInvestmentSocialLinkWriteRepository):
    def create(self, data: ProjectInvestmentSocialLinkCreatePayload) -> ProjectInvestmentSocialLink:
        return ProjectInvestmentSocialLink.objects.create(
            investment_id=data.investment_id.value,
            platform=data.social_link.platform,
            url=data.social_link.link,
        )

    def update(self, data: ProjectInvestmentSocialLinkUpdatePayload) -> ProjectInvestmentSocialLink:
        raise NotImplementedError("The method update() is not implemented yet.")

    def delete_by_id(self, id_: ProjectInvestmentSocialLinkId) -> None:
        raise NotImplementedError("The method delete_by_id() is not implemented yet.")

    def delete(self, investment: ProjectInvestmentSocialLink) -> None:
        investment.delete()


# ======================================================================================================================
class DjProjectInvestmentPhoneReadRepository(ProjectInvestmentPhoneReadRepository):
    def get_by_id(self, id_: ProjectInvestmentId) -> ProjectInvestment:
        raise NotImplementedError("The method get_by_id() is not implemented yet.")

    def get_all(
        self, filter_: ProjectInvestmentPhoneFilter, pagination: CursorPagination | OffsetPagination | None = None
    ) -> list[ProjectInvestmentPhone]:
        queryset = ProjectInvestmentPhone.objects.all()

        if filter_.number is not None:
            queryset = queryset.filter(number=filter_.number.value)

        if filter_.investment_id is not None:
            queryset = queryset.filter(investment_id=filter_.investment_id.value)

        if pagination:
            return apply_pagination(queryset=queryset, pagination=pagination)

        return list(queryset)


class DjProjectInvestmentPhoneWriteRepository(ProjectInvestmentPhoneWriteRepository):
    def create(self, data: ProjectInvestmentPhoneCreatePayload) -> ProjectInvestmentPhone:
        return ProjectInvestmentPhone.objects.create(
            investment_id=data.investment_id.value,
            number=data.phone_number.value,
        )

    def update(self, data: ProjectInvestmentPhoneUpdatePayload) -> ProjectInvestmentPhone:
        raise NotImplementedError("The method update() is not implemented yet.")

    def delete_by_id(self, id_: ProjectInvestmentId) -> None:
        raise NotImplementedError("The method delete_by_id() is not implemented yet.")

    def delete(self, investment_phone: ProjectInvestmentPhone) -> None:
        investment_phone.delete()
