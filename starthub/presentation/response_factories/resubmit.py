from presentation.response_factories.common import CommonErrorResponseFactory


class ProjectResubmitErrorResponseFactory(CommonErrorResponseFactory):
    error_codes = CommonErrorResponseFactory.error_codes | {}
