from dataclasses import dataclass

from domain.value_objects.user import Email, RawPassword


@dataclass(frozen=True)
class LoginCredentials:
    email: Email
    password: RawPassword
