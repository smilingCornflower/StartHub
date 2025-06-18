from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import QuerySet

from domain.models.user import User
from domain.models.role import Role

from typing import Any


class Command(BaseCommand):
    help = 'Assigns "user" role only to users with NO roles at all'

    def handle(self, *args: Any, **options: Any) -> None:
        try:
            user_role: Role = Role.objects.get(name='user')
        except Role.DoesNotExist:
            self.stderr.write('Error: Role "user" does not exist. Create it first.')
            return


        users_without_any_roles: QuerySet[User] = User.objects.filter(roles__isnull=True)
        count: int = users_without_any_roles.count()

        if not count:
            self.stdout.write('All users already have at least one role.')
            return

        self.stdout.write(f'Found {count} users without any roles...')

        with transaction.atomic():
            for user in users_without_any_roles:
                user.roles.add(user_role)

        self.stdout.write(
            self.style.SUCCESS(f'Added "user" role to {count} users with no roles')
        )