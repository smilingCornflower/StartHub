from dataclasses import dataclass
from datetime import date, datetime


@dataclass(frozen=True)
class UserDto:
    id: int
    first_name: str
    last_name: str
    email: str


@dataclass(frozen=True)
class UserFullDto(UserDto):
    date_joined: date
    roles: list[str]
    is_active: bool


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


@dataclass(frozen=True)
class UserMessageDto:
    id: int
    user_id: int
    first_name: str
    last_name: str
    email: str
    topic: str
    content: str
    created_at: datetime
