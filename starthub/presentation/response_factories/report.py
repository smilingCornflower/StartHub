from presentation.response_factories.common import CommonErrorResponseFactory


class ProjectReportErrorResponseFactory(CommonErrorResponseFactory):
    error_codes = CommonErrorResponseFactory.error_codes | {}
