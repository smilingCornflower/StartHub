from datetime import UTC, datetime

from domain.exceptions.user import UserNotFoundException
from domain.models.user_management.user import User, UserPhone
from domain.repositories.user_management.user import (
    UserPhoneReadRepository,
    UserPhoneWriteRepository,
    UserReadRepository,
    UserWriteRepository,
)
from domain.value_objects.common import CursorPagination, Id, OffsetPagination, PhoneNumber
from domain.value_objects.filter import UserFilter, UserPhoneFilter
from domain.value_objects.user_management.user import (
    Email,
    UserCreatePayload,
    UserPhoneCreatePayload,
    UserPhoneUpdatePayload,
    UserUpdatePayload,
)
from infrastructure.repositories.pagination import apply_pagination
from loguru import logger


class DjUserReadRepository(UserReadRepository):
    def get_by_id(self, id_: Id) -> User:
        """:raises UserNotFoundException:"""
        user: User | None = User.objects.filter(id=id_.value).first()

        if user is None:
            raise UserNotFoundException(f"An user with id = {id_.value} not found.")
        return user

    def get_all(self, filter_: UserFilter, pagination: CursorPagination | OffsetPagination | None = None) -> list[User]:
        queryset = User.objects.all()

        if filter_.id_:
            queryset = queryset.filter(id=filter_.id_.value)
        if filter_.email:
            queryset = queryset.filter(email=filter_.email.value)
        if filter_.first_name:
            queryset = queryset.filter(first_name__icontains=filter_.first_name.value)
        if filter_.last_name:
            queryset = queryset.filter(last_name__icontains=filter_.last_name.value)
        if filter_.role:
            queryset = queryset.filter(roles__name=filter_.role)
        if filter_.is_active is not None:
            queryset = queryset.filter(is_active=filter_.is_active)
        if filter_.date_joined_start:
            queryset = queryset.filter(date_joined__gte=filter_.date_joined_start)
        if filter_.date_joined_end:
            queryset = queryset.filter(date_joined__lte=filter_.date_joined_end)

        if pagination:
            return apply_pagination(queryset=queryset, pagination=pagination)

        return list(queryset.distinct())

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

        if data.first_name is not None:
            user.first_name = data.first_name.value
        if data.last_name is not None:
            user.last_name = data.last_name.value
        if data.description is not None:
            user.description = data.description.value
        if data.password is not None:
            user.set_password(data.password.value)
        if data.picture is not None:
            user.picture = data.picture
        if data.role_to_add is not None:
            user.roles.add(data.role_to_add)
        if data.role_to_remove is not None:
            user.roles.remove(data.role_to_remove)
        if data.is_active is not None:
            user.is_active = data.is_active

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


class DjUserPhoneReadRepository(UserPhoneReadRepository):
    def get_by_id(self, id_: Id) -> UserPhone:
        raise NotImplementedError("The method get_by_id() not implemented yet.")

    def get_all(
        self, filter_: UserPhoneFilter, pagination: CursorPagination | OffsetPagination | None = None
    ) -> list[UserPhone]:
        qs = UserPhone.objects.all()

        if filter_.user_id is not None:
            qs = qs.filter(user_id=filter_.user_id.value)
        if filter_.phone is not None:
            qs = qs.filter(number=filter_.phone.value)
        logger.debug(qs.query)
        return list(qs.distinct())


class DjUserPhoneWriteRepository(UserPhoneWriteRepository):
    def create(self, data: UserPhoneCreatePayload) -> UserPhone:
        return UserPhone.objects.create(user_id=data.user_id.value, number=data.phone.value)

    def update(self, data: UserPhoneUpdatePayload) -> UserPhone:
        raise NotImplementedError("The method update() not implemented yet.")

    def delete_by_id(self, id_: Id) -> None:
        raise NotImplementedError("The method delete_by_id() not implemented yet.")

    def delete_by_phone(self, phone: PhoneNumber) -> None:
        try:
            UserPhone.objects.get(number=phone.value).delete()
        except UserPhone.DoesNotExist:
            logger.info("Phone not found. Ignoring this exception as delete is idempotent.")
