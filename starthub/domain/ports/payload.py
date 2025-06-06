from abc import ABC

from domain.value_objects import BaseVo


class AbstractPayload(ABC, BaseVo):
    pass


class AbstractCreatePayload(AbstractPayload):
    pass


class AbstractUpdatePayload(AbstractPayload):
    pass


class AbstractDeletePayload(AbstractPayload):
    pass
