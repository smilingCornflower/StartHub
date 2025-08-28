from json import JSONDecodeError

from domain.exceptions.company import BusinessNumberAlreadyExistsException, CompanyNameIsTooLongException
from domain.exceptions.file import (
    ImageFileTooLargeException,
    NotPdfFileException,
    UnsupportedFileExtensionException,
    VideoFileTooLargeException,
)
from domain.exceptions.geo.city import CityNotFoundException
from domain.exceptions.geo.country import CountryNotFoundException, InvalidCountryCodeException
from domain.exceptions.geo.geo import GeographicalInconsistencyException
from domain.exceptions.geo.region import RegionNotFoundException
from domain.exceptions.project_management import (
    FundingModelNotFoundException,
    InvalidProjectStageException,
    InvalidProjectStatusException,
    NegativeProjectGoalSumException,
    ProjectAcceleratorAlreadyExists,
    ProjectAcceleratorNotFoundException,
    ProjectBankLoanMaxAmountException,
    ProjectBankLoanNotFoundException,
    ProjectBootstrapNotFoundException,
    ProjectCategoryNotFoundException,
    ProjectCrowdfundingAlreadyExistsException,
    ProjectCrowdfundingMaxAmountException,
    ProjectCrowdfundingNotFoundException,
    ProjectFileNotFoundException,
    ProjectGovernmentGrantMaxAmountException,
    ProjectGovernmentGrantNotFoundException,
    ProjectImageMaxAmountException,
    ProjectInvestmentDoesNotBelongToProjectException,
    ProjectInvestmentMaxAmountException,
    ProjectInvestmentNotFoundException,
    ProjectInvestmentPhoneAlreadyExistsException,
    ProjectInvestmentPhoneMaxAmountException,
    ProjectInvestmentPhoneNotFoundException,
    ProjectMediaMaxAmountException,
    ProjectMediaNotFoundException,
    ProjectNameIsTooLongException,
    ProjectNotFoundException,
    ProjectPlanNotFoundException,
    ProjectStageNotFoundException,
    ProjectStepMaxAmountException,
    ProjectUsefulLinkAlreadyExistsException,
    ProjectUsefulLinkMaxAmountException,
    ProjectUsefulLinkNotFoundException,
)
from domain.exceptions.validation import (
    DateInFutureException,
    DeadlineInPastException,
    DisallowedSocialLinkException,
    FirstNameIsTooLongException,
    InvalidPhoneNumberException,
    InvalidSocialLinkException,
    LastNameIsTooLongException,
    NegativeNumberException,
    StringIsTooLongException,
)
from presentation.response_factories.common import CommonErrorResponseFactory


class ProjectErrorResponseFactory(CommonErrorResponseFactory):
    error_codes = CommonErrorResponseFactory.error_codes | {
        ProjectNameIsTooLongException: ("PROJECT_NAME_TOO_LONG", 422),
        BusinessNumberAlreadyExistsException: ("BUSINESS_NUMBER_ALREADY_EXISTS", 409),
        ProjectCategoryNotFoundException: ("PROJECT_CATEGORY_NOT_FOUND", 404),
        FundingModelNotFoundException: ("FUNDING_MODEL_NOT_FOUND", 404),
        ProjectStageNotFoundException: ("PROJECT_STAGE_NOT_FOUND", 404),
        ProjectPlanNotFoundException: ("PROJECT_PLAN_NOT_FOUND", 404),
        CityNotFoundException: ("CITY_NOT_FOUND", 404),
        RegionNotFoundException: ("REGION_NOT_FOUND", 404),
        InvalidProjectStageException: ("INVALID_PROJECT_STAGE", 422),
        NegativeProjectGoalSumException: ("NEGATIVE_GOAL_SUM", 422),
        DisallowedSocialLinkException: ("DISALLOWED_SOCIAL_PLATFORM", 422),
        InvalidSocialLinkException: ("INVALID_SOCIAL_LINK", 422),
        JSONDecodeError: ("JSON_DECODE_ERROR", 400),
        InvalidPhoneNumberException: ("INVALID_PHONE_NUMBER", 422),
        NotPdfFileException: ("NOT_PDF_FILE", 400),
        StringIsTooLongException: ("STRING_TOO_LONG", 422),
        FirstNameIsTooLongException: ("FIRST_NAME_TOO_LONG", 422),
        LastNameIsTooLongException: ("LAST_NAME_TOO_LONG", 422),
        CompanyNameIsTooLongException: ("COMPANY_NAME_TOO_LONG", 422),
        InvalidCountryCodeException: ("INVALID_COUNTRY_CODE", 422),
        CountryNotFoundException: ("COUNTRY_NOT_FOUND", 404),
        DateInFutureException: ("DATE_IN_FUTURE_NOT_ALLOWED", 422),
        ProjectNotFoundException: ("PROJECT_NOT_FOUND", 404),
        DeadlineInPastException: ("DEADLINE_IN_PAST", 422),
        ProjectImageMaxAmountException: ("TOO_MANY_IMAGES", 422),
        ImageFileTooLargeException: ("IMAGE_TOO_LARGE", 422),
        InvalidProjectStatusException: ("INVALID_PROJECT_STATUS", 422),
        GeographicalInconsistencyException: ("GEOGRAPHICAL_INCONSISTENCY", 422),
        ProjectStepMaxAmountException: ("TOO_MANY_PROJECT_STEPS", 422),
        ProjectCrowdfundingMaxAmountException: ("MAX_CROWDFUNDING_AMOUNT_EXCEEDED", 422),
    }


class CompanyErrorResponseFactory(CommonErrorResponseFactory):
    error_codes = CommonErrorResponseFactory.error_codes | {}


class AcceleratorErrorResponseFactory(CommonErrorResponseFactory):
    error_codes = CommonErrorResponseFactory.error_codes | {
        ProjectAcceleratorAlreadyExists: ("PROJECT_ACCELERATOR_ALREADY_EXISTS", 409),
        ProjectAcceleratorNotFoundException: ("PROJECT_ACCELERATOR_NOT_FOUND", 404),
        ProjectNotFoundException: ("PROJECT_NOT_FOUND", 404),
    }


class CrowdfundingErrorResponseFactory(CommonErrorResponseFactory):
    error_codes = CommonErrorResponseFactory.error_codes | {
        ProjectCrowdfundingNotFoundException: ("PROJECT_CROWDFUNDING_NOT_FOUND", 404),
        ProjectCrowdfundingAlreadyExistsException: ("PROJECT_CROWDFUNDING_ALREADY_EXISTS", 409),
        ProjectNotFoundException: ("PROJECT_NOT_FOUND", 404),
    }


class ProjectInvestmentErrorResponseFactory(CommonErrorResponseFactory):
    error_codes = CommonErrorResponseFactory.error_codes | {
        DisallowedSocialLinkException: ("DISALLOWED_SOCIAL_PLATFORM", 422),
        StringIsTooLongException: ("STRING_TOO_LONG", 422),
        ProjectInvestmentMaxAmountException: ("MAX_INVESTMENT_AMOUNT_EXCEEDED", 422),
        ProjectNotFoundException: ("PROJECT_NOT_FOUND", 404),
        ProjectInvestmentDoesNotBelongToProjectException: ("INVESTMENT_DOES_NOT_BELONG_TO_PROJECT", 422),
        ProjectInvestmentNotFoundException: ("INVESTMENT_NOT_FOUND", 404),
        ProjectInvestmentPhoneAlreadyExistsException: ("INVESTMENT_PHONE_ALREADY_EXISTS", 409),
        ProjectInvestmentPhoneMaxAmountException: ("MAX_INVESTMENT_PHONE_AMOUNT_EXCEEDED", 422),
        ProjectInvestmentPhoneNotFoundException: ("INVESTMENT_PHONE_NOT_FOUND", 404),
    }


class ProjectGovernmentGrantErrorResponseFactory(CommonErrorResponseFactory):
    error_codes = CommonErrorResponseFactory.error_codes | {
        ProjectGovernmentGrantMaxAmountException: ("MAX_GOVERNMENT_GRANT_AMOUNT_EXCEEDED", 422),
        NegativeNumberException: ("NEGATIVE_NUMBER", 422),
        ProjectNotFoundException: ("PROJECT_NOT_FOUND", 404),
        ProjectGovernmentGrantNotFoundException: ("GOVERNMENT_GRANT_NOT_FOUND", 404),
        StringIsTooLongException: ("STRING_TOO_LONG", 422),
    }


class ProjectBootstrapErrorResponseFactory(CommonErrorResponseFactory):
    error_codes = CommonErrorResponseFactory.error_codes | {
        ProjectBootstrapNotFoundException: ("BOOTSTRAP_NOT_FOUND", 404),
    }


class ProjectBankLoanErrorResponseFactory(CommonErrorResponseFactory):
    error_codes = CommonErrorResponseFactory.error_codes | {
        ProjectBankLoanMaxAmountException: ("MAX_BANK_LOAN_AMOUNT_EXCEEDED", 422),
        ProjectBankLoanNotFoundException: ("BANK_LOAN_NOT_FOUND", 404),
        NegativeNumberException: ("NEGATIVE_NUMBER", 422),
        StringIsTooLongException: ("STRING_TOO_LONG", 422),
    }


class ProjectFileErrorResponseFactory(CommonErrorResponseFactory):
    error_codes = CommonErrorResponseFactory.error_codes | {
        ProjectNotFoundException: ("PROJECT_NOT_FOUND", 404),
        ProjectFileNotFoundException: ("PROJECT_FILE_NOT_FOUND", 404),
    }


class ProjectMediaErrorResponseFactory(CommonErrorResponseFactory):
    error_codes = CommonErrorResponseFactory.error_codes | {
        ProjectMediaNotFoundException: ("PROJECT_MEDIA_NOT_FOUND", 404),
        UnsupportedFileExtensionException: ("UNSUPPORTED_MEDIA_FORMAT", 422),
        ProjectMediaMaxAmountException: ("MAX_MEDIA_AMOUNT_EXCEEDED", 409),
        ImageFileTooLargeException: ("IMAGE_TOO_LARGE", 422),
        VideoFileTooLargeException: ("VIDEO_TOO_LARGE", 422),
    }


class ProjectUsefulLinkErrorResponseFactory(CommonErrorResponseFactory):
    error_codes = CommonErrorResponseFactory.error_codes | {
        ProjectUsefulLinkNotFoundException: ("PROJECT_USEFUL_LINK_NOT_FOUND", 404),
        ProjectUsefulLinkAlreadyExistsException: ("USEFUL_LINK_ALREADY_EXISTS", 409),
        ProjectUsefulLinkMaxAmountException: ("MAX_USEFUL_LINK_AMOUNT_EXCEEDED", 409),
    }


class ProjectStageErrorResponseFactory(CommonErrorResponseFactory):
    error_codes = CommonErrorResponseFactory.error_codes | {}
