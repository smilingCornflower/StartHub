from domain.exceptions.project_management import FundingModelNotFoundException
from domain.models.project_management.funding_model import FundingModel
from domain.repositories.project.funding_model import FundingModelReadRepository, FundingModelWriteRepository
from domain.value_objects.common import CursorPagination, Id, OffsetPagination
from domain.value_objects.filter import FundingModelFilter
from domain.value_objects.project.funding_model import (
    FundingModelCreatePayload,
    FundingModelId,
    FundingModelUpdatePayload,
)


class DjFundingModelReadRepository(FundingModelReadRepository):
    def get_by_id(self, id_: Id) -> FundingModel:
        """:raises FundingModelNotFoundException:"""
        funding_model: FundingModel | None = FundingModel.objects.filter(id=id_.value).first()
        if funding_model is None:
            raise FundingModelNotFoundException(f"Funding models with id = {id_.value} does not exist.")
        return funding_model

    def get_all(
        self, filter_: FundingModelFilter, pagination: CursorPagination | OffsetPagination | None = None
    ) -> list[FundingModel]:
        return list(FundingModel.objects.all())


class DjFundingModelWriteRepository(FundingModelWriteRepository):
    def create(self, data: FundingModelCreatePayload) -> FundingModel:
        raise NotImplementedError("The method create() is not implemented.")

    def update(self, data: FundingModelUpdatePayload) -> FundingModel:
        """:raises FundingModelNotFoundException:"""
        funding_model = FundingModel.objects.filter(id=data.id_.value).first()
        if funding_model is None:
            raise FundingModelNotFoundException(f"Funding model with id = {data.id_.value} not found.")

        if data.name:
            funding_model.name = data.name
            funding_model.slug = None
        if data.description:
            funding_model.description = data.description
        if data.recommended is not None:
            funding_model.recommended = data.recommended

        funding_model.save()
        return funding_model

    def delete_by_id(self, id_: FundingModelId) -> None:
        raise NotImplementedError("The method delete_by_id() is not implemented.")
