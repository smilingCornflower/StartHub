from domain.models.user import User
from domain.ports.filter import AbstractFilter
from domain.value_objects.common import FirstName, Id, LastName, PhoneNumber, Slug, SocialLink
from domain.value_objects.company import BusinessNumber
from domain.value_objects.country import CountryCode, CountryId
from domain.value_objects.geo import AddressId, CityId, RegionId
from domain.value_objects.project.common import ProjectStage, ProjectStatus
from domain.value_objects.project.investment import ProjectInvestmentId
from domain.value_objects.user import Email


class UserFilter(AbstractFilter):
    id_: Id | None = None
    first_name: FirstName | None = None
    last_name: LastName | None = None
    email: Email | None = None


class ProjectFilter(AbstractFilter):
    id_: Id | None = None
    id_list: list[Id] | None = None

    user_id: Id | None = None
    category_slug: Slug | None = None
    funding_model_slug: Slug | None = None
    status: ProjectStatus | None = None
    stage: ProjectStage | None = None


class ProjectCategoryFilter(AbstractFilter):
    project_id: Id | None = None
    category_ids: list[Id] | None = None


class FundingModelFilter(AbstractFilter):
    pass


class CompanyFilter(AbstractFilter):
    business_id: BusinessNumber | None = None


class CountryFilter(AbstractFilter):
    code: CountryCode


class TeamMemberFilter(AbstractFilter):
    pass


class ProjectPhoneFilter(AbstractFilter):
    project_id: Id | None = None
    number: PhoneNumber | None = None


class ProjectSocialLinkFilter(AbstractFilter):
    project_id: Id | None = None
    social_link: SocialLink | None = None


class CompanyFounderFilter(AbstractFilter):
    company_id: Id | None = None


class UserFavoriteFilter(AbstractFilter):
    user_id: Id | None = None
    project_id: Id | None = None


class ProjectImageFilter(AbstractFilter):
    project_id: Id | None = None
    image_order: int | None = None


class PermissionFilter(AbstractFilter):
    user_id: Id | None = None
    user: User | None = None


class RoleFilter(AbstractFilter):
    pass


class NewsFilter(AbstractFilter):
    pass


class UserPhoneFilter(AbstractFilter):
    user_id: Id | None = None
    phone: PhoneNumber | None = None


class NewsImageFilter(AbstractFilter):
    news_id: Id | None = None


class AddressFilter(AbstractFilter):
    address_id: AddressId | None = None
    country_id: CountryId | None = None
    region_id: RegionId | None = None
    city_id: CityId | None = None
    district: str | None = None
    street: str | None = None
    house_number: str | None = None
    postal_code: str | None = None
    raw_address: str | None = None


class CityFilter(AbstractFilter):
    pass


class RegionFilter(AbstractFilter):
    pass


class ProjectStepFilter(AbstractFilter):
    project_id: Id | None = None


class ProjectIncubatorFilter(AbstractFilter):
    project_id: Id | None = None


class ProjectAcceleratorFilter(AbstractFilter):
    project_id: Id | None = None


class ProjectCrowdfundingFilter(AbstractFilter):
    project_id: Id | None = None


class ProjectInvestmentFilter(AbstractFilter):
    project_id: Id | None = None


class ProjectInvestmentSocialLinkFilter(AbstractFilter):
    investment_id: ProjectInvestmentId | None = None


class ProjectInvestmentPhoneFilter(AbstractFilter):
    investment_id: ProjectInvestmentId | None = None
    number: PhoneNumber | None = None
