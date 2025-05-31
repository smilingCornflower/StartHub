from domain.ports.filter import AbstractFilter
from domain.value_objects.base import BaseVo
from domain.value_objects.common import Id, PhoneNumber, Slug, SocialLink
from domain.value_objects.country import CountryCode
from domain.value_objects.user import Email, Username


class UserFilter(AbstractFilter, BaseVo):
    id_: Id | None = None
    username: Username | None = None
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
    pass


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
