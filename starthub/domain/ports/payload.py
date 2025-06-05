from abc import ABC


class AbstractPayload(ABC):
    pass


class AbstractCreatePayload(AbstractPayload):
    pass


class AbstractUpdatePayload(AbstractPayload):
    pass


class AbstractDeletePayload(AbstractPayload):
    pass
