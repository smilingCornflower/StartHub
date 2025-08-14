from datetime import date

from domain.ports.command import BaseCommand
from domain.ports.payload import AbstractCreatePayload, AbstractUpdatePayload
from domain.value_objects import BaseVo
from domain.value_objects.common import DeadlineDate, Description, Id, PhoneNumber, SocialLink
from domain.value_objects.company import (
    BusinessNumber,
    CompanyFounderCreateCommand,
    CompanyName,
    EstablishedDate,
    PatentNumber,
)
from domain.value_objects.country import CountryCode
from domain.value_objects.file import ImageFile, PdfFile
from domain.value_objects.geo import AddressCreateCommand
from domain.value_objects.project.accelerator import ProjectAcceleratorCreateCommand
from domain.value_objects.project.bank_loan import ProjectBankLoanCreateCommand
from domain.value_objects.project.bootstrap import ProjectBootstrapCreateCommand
from domain.value_objects.project.common import GoalSum, ProjectName, ProjectStage, ProjectStatus
from domain.value_objects.project.crowdfunding import ProjectCrowdfundingCreateCommand
from domain.value_objects.project.government_grant import ProjectGovernmentGrantCreateCommand
from domain.value_objects.project.incubator import IncubatorCreateCommand, IncubatorUpdatePayload
from domain.value_objects.project.investment import ProjectInvestmentCreateCommand
from domain.value_objects.project.step import ProjectStepCreateCommand
from domain.value_objects.project.team_member import TeamMemberCreateCommand


class ProjectCreateCommand(BaseCommand):
    name: ProjectName
    goal_description: Description | None = None
    description: Description
    category_ids: list[Id]
    creator_id: Id
    funding_model_id: Id
    stage: ProjectStage
    steps: list[ProjectStepCreateCommand]
    goal_sum: GoalSum
    deadline: DeadlineDate
    social_links: list[SocialLink]
    phone_number: PhoneNumber
    plan_file: PdfFile
    images: list[ImageFile]

    incubator: IncubatorCreateCommand | None
    accelerator: ProjectAcceleratorCreateCommand | None
    crowdunding: ProjectCrowdfundingCreateCommand | None
    investment: ProjectInvestmentCreateCommand | None
    government_grant: ProjectGovernmentGrantCreateCommand | None
    bootstrap: ProjectBootstrapCreateCommand | None
    bank_loan: ProjectBankLoanCreateCommand | None

    company_name: CompanyName
    country_code: CountryCode
    company_address: AddressCreateCommand
    business_id: BusinessNumber
    established_date: EstablishedDate
    patent_number: PatentNumber | None

    team_members: list[TeamMemberCreateCommand]
    company_founder: CompanyFounderCreateCommand


class ProjectUpdateCommand(BaseCommand):
    project_id: Id
    user_id: Id
    name: ProjectName | None = None
    goal_description: Description | None = None
    description: Description | None = None
    category_ids: list[Id] | None = None
    funding_model_id: Id | None = None
    stage: ProjectStage | None = None
    goal_sum: GoalSum | None = None
    deadline: DeadlineDate | None = None
    plan_file: PdfFile | None = None
    steps: list[ProjectStepCreateCommand] | None = None

    incubator: IncubatorUpdatePayload | None = None


class ProjectCreatePayload(AbstractCreatePayload, BaseVo):
    name: ProjectName
    goal_description: Description | None = None
    description: Description
    category_ids: list[Id]
    user_id: Id
    funding_model_id: Id
    stage: ProjectStage
    status: ProjectStatus
    goal_sum: GoalSum
    deadline: date
    plan_path: str


class ProjectUpdatePayload(AbstractUpdatePayload, BaseVo):
    id_: Id
    name: ProjectName | None = None
    goal_description: Description | None = None
    description: Description | None = None
    category_ids: list[Id] | None = None
    funding_model_id: Id | None = None
    goal_sum: GoalSum | None = None
    stage: ProjectStage | None = None
    deadline: DeadlineDate | None = None
    plan_path: str | None = None
