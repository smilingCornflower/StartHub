from domain.ports.payload import AbstractCreatePayload, AbstractUpdatePayload
from domain.value_objects.base import BaseVo
from domain.value_objects.common import Id, PhoneNumber


class ProjectPhoneCreatePayload(AbstractCreatePayload, BaseVo):
    project_id: Id
    number: PhoneNumber


class ProjectPhoneUpdatePayload(AbstractUpdatePayload, BaseVo):
    phone_id: Id
    number: PhoneNumber
