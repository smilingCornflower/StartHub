from application.dto.user import UserProfileDto
from domain.value_objects.user import UserProfile


def user_profile_to_dto(profile: UserProfile) -> UserProfileDto:
    return UserProfileDto(
        id=profile.id_.value,
        first_name=profile.first_name.value,
        last_name=profile.last_name.value,
        email=profile.email.value,
        picture=profile.picture,
    )
