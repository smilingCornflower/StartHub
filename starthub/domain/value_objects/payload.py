from dataclasses import dataclass

from domain.ports.payload import AbstractCreatePayload, AbstractUpdatePayload
from domain.value_objects.common import Id
from domain.value_objects.user import Email, RawPassword, Username


@dataclass(frozen=True)
class UserCreatePayload(AbstractCreatePayload):
    username: Username
    email: Email
    password: RawPassword


@dataclass(frozen=True)
class UserUpdatePayload(AbstractUpdatePayload):
    id_: Id
    username: Username | None = None
    email: Email | None = None
    password: RawPassword | None = None
