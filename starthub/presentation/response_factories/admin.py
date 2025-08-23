from domain.exceptions.project_management import (
    ProjectAlreadyDeactivatedException,
    ProjectNotFoundException,
    ProjectSubmissionAlreadyProcessedException,
)
from domain.exceptions.role import RoleNotFoundException
from presentation.response_factories.common import CommonErrorResponseFactory


class ProjectSubmissionErrorResponseFactory(CommonErrorResponseFactory):
    error_codes = CommonErrorResponseFactory.error_codes | {
        ProjectSubmissionAlreadyProcessedException: ("PROJECT_SUBMISSION_ALREADY_PROCESSED", 409),
        ProjectAlreadyDeactivatedException: ("PROJECT_ALREADY_DEACTIVATED", 409),
        ProjectNotFoundException: ("PROJECT_NOT_FOUND", 404),
    }


class UsersAdminErrorResponseFactory(CommonErrorResponseFactory):
    error_codes = CommonErrorResponseFactory.error_codes | {
        RoleNotFoundException: ("ROLE_NOT_FOUND", 404),
    }
