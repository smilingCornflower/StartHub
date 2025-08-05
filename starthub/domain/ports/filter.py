from abc import ABC

from domain.value_objects import BaseVo


class AbstractFilter(ABC, BaseVo):
    model_config = {"arbitrary_types_allowed": True}
