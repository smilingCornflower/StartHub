from domain.enums.role import RoleEnum
from domain.ports.command import BaseCommand


class UserAdminUpdateCommand(BaseCommand):
    add_role: RoleEnum | None = None
    remove_role: RoleEnum | None = None
