from domain.ports.filter import AbstractFilter
from domain.value_objects import BaseVo
from domain.value_objects.common import FirstName, Id, LastName, PhoneNumber, Slug, SocialLink
from domain.value_objects.company import BusinessNumber
from domain.value_objects.country import CountryCode
from domain.value_objects.user import Email


class UserFilter(AbstractFilter, BaseVo):
    id_: Id | None = None
    first_name: FirstName | None = None
    last_name: LastName | None = None
    email: Email | None = None


class ProjectFilter(AbstractFilter, BaseVo):
    id_: Id | None = None
    category_slug: Slug | None = None
    funding_model_slug: Slug | None = None


class ProjectCategoryFilter(AbstractFilter, BaseVo):
    pass


class FundingModelFilter(AbstractFilter, BaseVo):
    pass


class CompanyFilter(AbstractFilter, BaseVo):
    business_id: BusinessNumber | None = None


class CountryFilter(AbstractFilter, BaseVo):
    code: CountryCode


class TeamMemberFilter(AbstractFilter, BaseVo):
    pass


class ProjectPhoneFilter(AbstractFilter, BaseVo):
    project_id: Id | None = None
    number: PhoneNumber | None = None


class ProjectSocialLinkFilter(AbstractFilter, BaseVo):
    project_id: Id | None = None
    social_link: SocialLink | None = None


class CompanyFounderFilter(AbstractFilter, BaseVo):
    company_id: Id | None = None
