from typing import Any, List, Type

from django.core.management.base import BaseCommand
from django.db import models
from domain.enums.permission import ActionEnum, ScopeEnum
from domain.enums.role import RoleEnum
from domain.models import ProjectIncubator
from domain.models.permission import Permission
from domain.models.project_management.accelerator import ProjectAccelerator
from domain.models.project_management.crowdfunding import ProjectCrowdfunding
from domain.models.project_management.investment import ProjectInvestment
from domain.models.project_management.project import Project
from domain.models.role import Role
from domain.services.permission import PermissionService
from domain.value_objects.user import PermissionVo
from loguru import logger


class Command(BaseCommand):
    help = "Assigns project permissions for user"

    def handle(self, *args: Any, **options: Any) -> None:
        self.assing_project_permissions_for_users()
        self._assign_project_accelerator_permission_for_users()
        self._assign_project_incubator_permission_for_users()
        self._assign_project_crowdfunding_permission_for_users()
        self._assign_project_investment_permission_for_users()

    def _assign_permissions_for_model(
            self,
            model: Type[models.Model],
            actions: List[ActionEnum],
            log_start_message: str,
            log_end_message: str
    ) -> None:
        """Helper method to assign permissions for a given model."""
        logger.warning(log_start_message)

        for action in actions:
            permission_vo: PermissionVo = PermissionService.create_permission_vo(
                model=model, action=action, scope=ScopeEnum.OWN
            )
            permission, _ = Permission.objects.get_or_create(name=permission_vo.value)

            user_role, _ = Role.objects.get_or_create(name=RoleEnum.USER)
            user_role.permissions.add(permission)

        logger.info(log_end_message)

    def assing_project_permissions_for_users(self) -> None:
        self._assign_permissions_for_model(
            model=Project,
            actions=[ActionEnum.CHANGE, ActionEnum.DELETE],
            log_start_message="Started command: assing_project_permissions_for_users()",
            log_end_message="User permissions for project initialized"
        )

    def _assign_project_investment_permission_for_users(self) -> None:
        self._assign_permissions_for_model(
            model=ProjectInvestment,
            actions=[ActionEnum.ADD, ActionEnum.CHANGE, ActionEnum.DELETE],
            log_start_message="Started command: _assign_project_investment_permission_for_users()",
            log_end_message="User permissions for project investment initialized"
        )

    def _assign_project_accelerator_permission_for_users(self) -> None:
        self._assign_permissions_for_model(
            model=ProjectAccelerator,
            actions=[ActionEnum.ADD, ActionEnum.CHANGE, ActionEnum.DELETE],
            log_start_message="Started command: _assign_project_accelerator_permission_for_users()",
            log_end_message="User permissions for project accelerator initialized"
        )

    def _assign_project_incubator_permission_for_users(self) -> None:
        self._assign_permissions_for_model(
            model=ProjectIncubator,
            actions=[ActionEnum.ADD, ActionEnum.CHANGE, ActionEnum.DELETE],
            log_start_message="Started _assign_project_incubator_permission_for_users()",
            log_end_message="User permissions for project incubator initialized"
        )

    def _assign_project_crowdfunding_permission_for_users(self) -> None:
        self._assign_permissions_for_model(
            model=ProjectCrowdfunding,
            actions=[ActionEnum.ADD, ActionEnum.CHANGE, ActionEnum.DELETE],
            log_start_message="Started _assign_project_crowdfunding_permission_for_users()",
            log_end_message="User permissions for project crowdfunding initialized"
        )