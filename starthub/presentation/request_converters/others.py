from domain.exceptions.project_management import FundingModelNotFoundException
from presentation.response_factories.common import CommonErrorResponseFactory


class FundingModelErrorResponseFactory(CommonErrorResponseFactory):
    error_codes = CommonErrorResponseFactory.error_codes | {
        FundingModelNotFoundException: ("FUNDING_MODEL_NOT_FOUND", 404),
    }
