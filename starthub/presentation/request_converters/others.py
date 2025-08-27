from presentation.response_factories.common import CommonErrorResponseFactory


class FundingModelErrorResponseFactory(CommonErrorResponseFactory):
    error_codes = CommonErrorResponseFactory.error_codes | {}
