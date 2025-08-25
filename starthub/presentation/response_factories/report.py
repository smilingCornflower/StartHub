from domain.exceptions.project_management import ProjectResubmitException
from presentation.response_factories.common import CommonErrorResponseFactory


class ProjectReportErrorResponseFactory(CommonErrorResponseFactory):
    error_codes = CommonErrorResponseFactory.error_codes | {
        ProjectResubmitException: ("PROJECT_RESUBMIT_ERROR", 409),
    }
