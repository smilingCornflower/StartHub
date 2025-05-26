from dataclasses import dataclass

from domain.ports.filter import AbstractFilter
from domain.value_objects.common import Id, Slug
from domain.value_objects.user import Email, Username


@dataclass(frozen=True)
class UserFilter(AbstractFilter):
    id_: Id | None = None
    username: Username | None = None
    email: Email | None = None


@dataclass(frozen=True)
class ProjectFilter(AbstractFilter):
    category_slug: Slug | None = None
