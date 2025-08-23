from application.ports.service import AbstractAppService
from domain.enums.role import RoleEnum
from domain.repositories.role import RoleReadRepository
from domain.repositories.user import UserReadRepository
from domain.services.users_management.admin import UserAdminService
from domain.value_objects.common import Id
from domain.value_objects.user_management.admin import UserAdminUpdateCommand


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
