from dataclasses import dataclass


@dataclass
class UserProfileDto:
    id: int
    first_name: str
    last_name: str
    email: str
    picture: str | None


@dataclass
class UserFavoriteDto:
    user_id: int
    project_id: int
