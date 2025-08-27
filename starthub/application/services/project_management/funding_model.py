from application.ports.service import AbstractAppService
from domain.repositories.project.funding_model import FundingModelReadRepository
from domain.repositories.user_management.user import UserReadRepository
from domain.services.project_management.funding_model import FundingModelService
from domain.value_objects.common import Id
from domain.value_objects.project.funding_model import (
    FundingModelId,
    FundingModelUpdateCommand,
    FundingModelUpdatePayload,
)


class FundingModelAppService(AbstractAppService):
    def __init__(
        self,
        funding_model_service: FundingModelService,
        user_read_repository: UserReadRepository,
        funding_model_read_repository: FundingModelReadRepository,
    ):
        self._funding_model_service = funding_model_service
        self._user_read_repository = user_read_repository
        self._funding_model_read_repository = funding_model_read_repository

    def update(self, user_id: Id, funding_model_id: FundingModelId, command: FundingModelUpdateCommand) -> None:
        user = self._user_read_repository.get_by_id(id_=user_id)
        self._funding_model_read_repository.get_by_id(id_=funding_model_id)
        payload = FundingModelUpdatePayload(
            id_=funding_model_id,
            name=command.name,
            description=command.description,
            recommended=command.recommended,
        )
        self._funding_model_service.update(user=user, payload=payload)
