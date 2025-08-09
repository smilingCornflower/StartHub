from domain.exceptions import CustomException
from domain.exceptions.repository import AlreadyExistsException, NotFoundException
from domain.exceptions.validation import NegativeNumberException, ValidationException


class ProjectException(CustomException):
    pass


class ProjectCategoryException(ProjectException):
    pass


class ProjectCategoryNotFoundException(NotFoundException, ProjectCategoryException):
    pass


class ProjectPhoneException(ProjectException):
    pass


class ProjectPhoneAlreadyExistsException(AlreadyExistsException, ProjectPhoneException):
    pass


class ProjectPhoneNotFoundException(NotFoundException, ProjectPhoneException):
    pass


class ProjectNameIsTooLongException(ValidationException, ProjectException):
    pass


class NegativeProjectGoalSumException(NegativeNumberException, ProjectException):
    pass


class ProjectNotFoundException(NotFoundException, ProjectException):
    pass


class ProjectNameAlreadyExistsException(AlreadyExistsException, ProjectException):
    pass


class ProjectPlanNotFoundException(NotFoundException, ProjectException):
    pass


# ==== Project Image Exceptions ====
class ProjectImageException(ProjectException):
    pass


class ProjectImageMaxAmountException(ProjectImageException):
    pass


class ProjectImageNotFoundException(NotFoundException, ProjectImageException):
    pass


# ==== Funding Model Exceptions ====
class FundingModelException(ProjectException):
    pass


class FundingModelNotFoundException(NotFoundException, FundingModelException):
    pass


# ==== Team Member Exceptions ====
class TeamMemberException(ProjectException):
    pass


class TeamMemberNotFoundException(NotFoundException, TeamMemberException):
    pass


# ==== Project Social Link Exceptions ====
class ProjectSocialLinkException(ProjectException):
    pass


class ProjectSocialLinkNotFoundException(NotFoundException, ProjectSocialLinkException):
    pass


class ProjectSocialLinkAlreadyExistsException(AlreadyExistsException, ProjectSocialLinkException):
    pass


# ==== Project Stage Exceptions ====
class ProjectStageException(ProjectException):
    pass


class InvalidProjectStageException(ValidationException, ProjectStageException):
    pass


# ==== Project Status Exceptions ====
class ProjectStatusException(ProjectException):
    pass


class InvalidProjectStatusException(ValidationException, ProjectStatusException):
    pass


# ==== Project Steps Exceptions ====
class ProjectStepException(ProjectException):
    pass


class ProjectStepMaxAmountException(ProjectStepException):
    pass


# ==== Project Incubator Exceptions ====
class ProjectIncubatorException(ProjectException):
    pass


class ProjectIncubatorNotFoundException(ProjectIncubatorException, NotFoundException):
    pass


# ==== Project Accelerator Exceptions ====
class ProjectAcceleratorException(ProjectException):
    pass


class ProjectAcceleratorNotFoundException(ProjectAcceleratorException, NotFoundException):
    pass


# ==== Project Crowdfunding Exceptions ====
class ProjectCrowdfundingException(ProjectException):
    pass


class ProjectCrowdfundingMaxAmountException(ValidationException, ProjectCrowdfundingException):
    pass
