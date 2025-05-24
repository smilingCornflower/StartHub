from dataclasses import dataclass

from domain.ports.filter import AbstractFilter
from domain.value_objects.common import Id
from domain.value_objects.user import Email, Username


@dataclass
class UserFilter(AbstractFilter):
    id_: Id | None = None
    username: Username | None = None
    email: Email | None = None
