from dataclasses import dataclass


@dataclass(frozen=True)
class UserDto:
    id: int
    first_name: str
    last_name: str
    email: str


@dataclass
class UserProfileDto:
    id: int
    first_name: str
    last_name: str
    description: str
    email: str
    picture: str | None
    phone_numbers: list[str]


@dataclass
class UserFavoriteDto:
    user_id: int
    project_id: int
