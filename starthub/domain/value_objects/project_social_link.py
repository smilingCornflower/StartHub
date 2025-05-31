from domain.ports.payload import AbstractCreatePayload, AbstractUpdatePayload
from domain.value_objects.base import BaseVo
from domain.value_objects.common import Id, SocialLink


class ProjectSocialLinkCreatePayload(AbstractCreatePayload, BaseVo):
    project_id: Id
    social_link: SocialLink


class ProjectSocialLinkUpdatePayload(AbstractUpdatePayload, BaseVo):
    project_id: Id
    social_link: SocialLink
