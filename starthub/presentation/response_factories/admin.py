from domain.exceptions.project_management import ProjectNotFoundException, ProjectSubmissionAlreadyProcessedException
from presentation.response_factories.common import CommonErrorResponseFactory


class ProjectSubmissionErrorResponseFactory(CommonErrorResponseFactory):
    error_codes = CommonErrorResponseFactory.error_codes | {
        ProjectSubmissionAlreadyProcessedException: ("PROJECT_SUBMISSION_ALREADY_PROCESSED", 409),
        ProjectNotFoundException: ("PROJECT_NOT_FOUND", 404),
    }
