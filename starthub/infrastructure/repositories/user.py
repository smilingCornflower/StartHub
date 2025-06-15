from datetime import UTC, datetime

from domain.exceptions.user import UserNotFoundException
from domain.models.user import User
from domain.repositories.user import UserReadRepository, UserWriteRepository
from domain.value_objects.common import Id
from domain.value_objects.filter import UserFilter
from domain.value_objects.user import Email, UserCreatePayload, UserUpdatePayload


class DjUserReadRepository(UserReadRepository):
    def get_by_id(self, id_: Id) -> User:
        """:raises UserNotFoundException:"""
        user: User | None = User.objects.filter(id=id_.value).first()

        if user is None:
            raise UserNotFoundException(f"An user with id = {id_.value} not found.")
        return user

    def get_all(self, filter_: UserFilter) -> list[User]:
        if filter_.id_:
            return list(User.objects.filter(id=filter_.id_.value))
        if filter_.email:
            return list(User.objects.filter(email=filter_.email.value))
        if filter_.first_name:
            return list(User.objects.filter(username=filter_.first_name.value))
        if filter_.last_name:
            return list(User.objects.filter(username=filter_.last_name.value))
        return list(User.objects.all())

    def get_by_email(self, email: Email) -> User:
        """:raises UserNotFoundException:"""
        user: User | None = User.objects.filter(email=email.value).first()
        if user is None:
            raise UserNotFoundException(f"An user with email = {email.value} not found.")
        return user


class DjUserWriteRepository(UserWriteRepository):
    def create(self, data: UserCreatePayload) -> User:
        return User.objects.create_user(
            email=data.email.value,
            password=data.password.value,
        )

    def update(self, data: UserUpdatePayload) -> User:
        """:raises UserNotFoundException:"""
        try:
            user: User = User.objects.get(id=data.id_.value)
        except User.DoesNotExist:
            raise UserNotFoundException(f"An user with id = {data.id_.value} is not found.")

        if data.first_name:
            user.first_name = data.first_name.value
        if data.last_name:
            user.last_name = data.last_name.value
        if data.password:
            user.set_password(data.password.value)
        if data.picture:
            user.picture = data.picture
        user.save()
        return user

    def delete_by_id(self, id_: Id) -> None:
        """:raises UserNotFoundException:"""
        try:
            User.objects.get(id=id_.value).delete()
        except User.DoesNotExist:
            raise UserNotFoundException(f"An user with id = {id_.value} is not found.")

    def update_last_login(self, user: User) -> None:
        user.last_login = datetime.now(UTC)
        user.save()
