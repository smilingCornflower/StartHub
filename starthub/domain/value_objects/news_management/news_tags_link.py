from domain.ports.payload import AbstractCreatePayload, AbstractUpdatePayload
from domain.value_objects.common import Id


class NewsTagsLinkCreatePayload(AbstractCreatePayload):
    news_id: Id
    news_tag_id: Id


class NewsTagsLinkUpdatePayload(AbstractUpdatePayload):
    pass
