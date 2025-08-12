from domain.ports.payload import AbstractCreatePayload
from domain.value_objects.common import Id, SocialLink
from domain.value_objects.geo import AddressUpdatePayload
from domain.value_objects.project.investment import ProjectInvestmentId


class ProjectInvestmentSocialLinkId(Id):
    pass


class ProjectInvestmentSocialLinkCreatePayload(AbstractCreatePayload):
    investment_id: ProjectInvestmentId
    social_link: SocialLink


class ProjectInvestmentSocialLinkUpdatePayload(AddressUpdatePayload):
    investment_id: ProjectInvestmentId
    social_link: SocialLink
