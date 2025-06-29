from dataclasses import dataclass


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
