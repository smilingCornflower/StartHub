from abc import abstractmethod

from django.db import models
from domain.ports.model import AbstractModel


class BaseModel(models.Model, AbstractModel):
    id: int

    class Meta:
        abstract = True

    @abstractmethod
    def __str__(self) -> str:
        pass

    @classmethod
    @abstractmethod
    def get_permission_key(cls) -> str:
        """
        Static identifier used as the model's permission key in the authorization system.

        This key serves as the immutable model reference in permission strings
        (e.g. 'action.scope.<key>.field'). When implemented:
        1. MUST return a constant string (unaffected by class renaming)
        2. MUST be unique per model within the application

        :returns str: Model's permission key (e.g. 'social_link', 'user_profile')
        """
        pass
