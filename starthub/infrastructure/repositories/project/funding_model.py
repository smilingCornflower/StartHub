from domain.exceptions.project_management import FundingModelNotFoundException
from domain.models.project_management.funding_model import FundingModel
from domain.repositories.project.funding_model import FundingModelReadRepository
from domain.value_objects.common import Id, Pagination
from domain.value_objects.filter import FundingModelFilter


class DjFundingModelReadRepository(FundingModelReadRepository):
    def get_by_id(self, id_: Id) -> FundingModel:
        """:raises FundingModelNotFoundException:"""
        funding_model: FundingModel | None = FundingModel.objects.filter(id=id_.value).first()
        if funding_model is None:
            raise FundingModelNotFoundException(f"Funding models with id = {id_.value} does not exist.")
        return funding_model

    def get_all(self, filter_: FundingModelFilter, pagination: Pagination | None = None) -> list[FundingModel]:
        return list(FundingModel.objects.all())
