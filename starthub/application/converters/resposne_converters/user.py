from application.dto.user import UserFavoriteDto, UserProfileDto
from domain.models.user_favorite import UserFavorite
from domain.value_objects.user import UserProfile


def user_profile_to_dto(profile: UserProfile) -> UserProfileDto:
    return UserProfileDto(
        id=profile.id_.value,
        first_name=profile.first_name.value,
        last_name=profile.last_name.value,
        description=profile.description.value,
        email=profile.email.value,
        picture=profile.picture,
        phone_numbers=[i.value for i in profile.phone_numbers],
    )


def user_favorite_to_dto(user_favorite: UserFavorite) -> UserFavoriteDto:
    return UserFavoriteDto(
        user_id=user_favorite.user.id,
        project_id=user_favorite.project.id,
    )
