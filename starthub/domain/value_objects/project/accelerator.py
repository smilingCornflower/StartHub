from domain.ports.payload import AbstractCreatePayload
from domain.value_objects.common import Id
from domain.value_objects.geo import AddressUpdatePayload


class AcceleratorId(Id):
    pass


class ProjectAcceleratorCreatePayload(AbstractCreatePayload):
    pass


class ProjectAcceleratorUpdatePayload(AddressUpdatePayload):
    pass
