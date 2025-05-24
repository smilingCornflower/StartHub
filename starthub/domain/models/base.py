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
