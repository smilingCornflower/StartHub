from application.dto.user import UserFullDto
from application.ports.service import AbstractAppService
from domain.enums.role import RoleEnum
from domain.models.user_management.user import User
from domain.repositories.role import RoleReadRepository
from domain.repositories.user_management.user import UserReadRepository
from domain.services.users_management.user_admin import UserAdminService
from domain.value_objects.common import Id, Pagination
from domain.value_objects.filter import UserFilter
from domain.value_objects.user_management.user import UserGetCommand
from domain.value_objects.user_management.user_admin import UserAdminUpdateCommand
from loguru import logger


class UserAdminAppService(AbstractAppService):
    def __init__(
        self,
        user_admin_service: UserAdminService,
        user_read_repository: UserReadRepository,
        role_read_repository: RoleReadRepository,
    ):
        self._user_admin_service = user_admin_service
        self._user_read_repository = user_read_repository
        self._role_read_repository = role_read_repository

    def change_user_role(self, call_user_id: Id, target_user_id: Id, command: UserAdminUpdateCommand) -> None:
        if command.add_role:
            self._add_user_role(call_user_id=call_user_id, target_user_id=target_user_id, role_name=command.add_role)
        if command.remove_role:
            self.remove_user_role(
                call_user_id=call_user_id, target_user_id=target_user_id, role_name=command.remove_role
            )

    def _add_user_role(self, call_user_id: Id, target_user_id: Id, role_name: RoleEnum) -> None:
        call_user = self._user_read_repository.get_by_id(id_=call_user_id)
        target_user = self._user_read_repository.get_by_id(id_=target_user_id)
        role = self._role_read_repository.get_by_name(name=role_name)

        self._user_admin_service.add_role_to_user(caller_user=call_user, target_user=target_user, role=role)

    def remove_user_role(self, call_user_id: Id, target_user_id: Id, role_name: RoleEnum) -> None:
        call_user = self._user_read_repository.get_by_id(id_=call_user_id)
        target_user = self._user_read_repository.get_by_id(id_=target_user_id)
        role = self._role_read_repository.get_by_name(name=role_name)

        self._user_admin_service.remove_role_form_user(caller_user=call_user, target_user=target_user, role=role)

    def activate_user(self, call_user_id: Id, target_user_id: Id) -> None:
        call_user = self._user_read_repository.get_by_id(id_=call_user_id)
        target_user = self._user_read_repository.get_by_id(id_=target_user_id)
        self._user_admin_service.activate(caller_user=call_user, target_user=target_user)

    def deactivate_user(self, call_user_id: Id, target_user_id: Id) -> None:
        call_user = self._user_read_repository.get_by_id(id_=call_user_id)
        target_user = self._user_read_repository.get_by_id(id_=target_user_id)
        self._user_admin_service.deactivate(caller_user=call_user, target_user=target_user)


class UserAdminGetAppService(AbstractAppService):
    def __init__(
        self,
        user_read_repository: UserReadRepository,
        user_admin_service: UserAdminService,
    ):
        self._user_admin_service = user_admin_service
        self._user_read_repository = user_read_repository

    def get_all(self, user_id: Id, command: UserGetCommand, pagination: Pagination) -> list[UserFullDto]:
        user = self._user_read_repository.get_by_id(id_=user_id)
        self._user_admin_service.check_permission_to_view_any_user_details(user=user)

        user_filter = self._convert_get_command_to_filter(command=command)
        users = self._user_read_repository.get_all(filter_=user_filter, pagination=pagination)
        logger.debug(f"Found {len(users)} users.")

        return [self._create_full_dto(user=user) for user in users]

    def _create_full_dto(self, user: User) -> UserFullDto:
        return UserFullDto(
            id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            date_joined=user.date_joined,
            roles=user.get_roles(),
            is_active=user.is_active,
        )

    def _convert_get_command_to_filter(self, command: UserGetCommand) -> UserFilter:
        return UserFilter(
            first_name=command.first_name,
            last_name=command.last_name,
            email=command.email,
            role=command.role,
            is_active=command.is_active,
            date_joined_start=command.date_joined_start,
            date_joined_end=command.date_joined_end,
        )
