from presentation.response_factories.common import CommonErrorResponseFactory


class ProjectSubmissionErrorResponseFactory(CommonErrorResponseFactory):
    error_codes = CommonErrorResponseFactory.error_codes | {}
