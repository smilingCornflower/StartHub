from domain.value_objects import BaseVo
from domain.value_objects.common import StringVo


class AnonymousId(StringVo):
    """
    Example `anon:38371158-982c-4db7-90c5-b2e350c0a01f`
    """

    pass


class AnonymousUser(BaseVo):
    id: AnonymousId
