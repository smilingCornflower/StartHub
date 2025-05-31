from domain.exceptions.funding_model import FundingModelNotFoundException
from domain.models.funding_model import FundingModel
from domain.repositories.funding_model import FundingModelReadRepository
from domain.value_objects.common import Id
from domain.value_objects.filter import FundingModelFilter


class DjFundingModelReadRepository(FundingModelReadRepository):
    def get_by_id(self, id_: Id) -> FundingModel:
        """:raises FundingModelNotFoundException:"""
        funding_model: FundingModel | None = FundingModel.objects.filter(id=id_.value).first()
        if funding_model is None:
            raise FundingModelNotFoundException(f"Funding models with id = {id_.value} does not exist.")
        return funding_model

    def get_all(self, filter_: FundingModelFilter) -> list[FundingModel]:
        return list(FundingModel.objects.all())
