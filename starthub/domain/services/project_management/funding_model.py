from domain.enums.permission import ActionEnum, ScopeEnum
from domain.exceptions.permissions import UpdateDeniedPermissionException
from domain.models.project_management.funding_model import FundingModel
from domain.models.user_management.user import User
from domain.ports.service import AbstractDomainService
from domain.repositories.project.funding_model import FundingModelWriteRepository
from domain.services.permission import PermissionService
from domain.value_objects.project.funding_model import FundingModelUpdatePayload
from loguru import logger


class FundingModelPermissionService(AbstractDomainService):
    def __init__(self, permission_service: PermissionService):
        self._permission_service = permission_service

    def _check_permission_to_change_any_funding_model(self, user: User) -> None:
        """:raises UpdateDeniedPermissionException:"""
        if self._permission_service.is_allowed_for_user(
            user=user,
            model=FundingModel,
            action=ActionEnum.CHANGE,
            scope=ScopeEnum.ANY,
        ):
            return None
        raise UpdateDeniedPermissionException("You don't have enough permission to funding model fields.")


class FundingModelService(FundingModelPermissionService):
    def __init__(
        self,
        permission_service: PermissionService,
        write_repository: FundingModelWriteRepository,
    ):
        super().__init__(permission_service=permission_service)
        self._write_repository = write_repository

    def update(self, user: User, payload: FundingModelUpdatePayload) -> None:
        self._check_permission_to_change_any_funding_model(user=user)
        self._write_repository.update(data=payload)
        logger.info(f"FundingModel(id={payload.id_.value}) updated successfully.")
