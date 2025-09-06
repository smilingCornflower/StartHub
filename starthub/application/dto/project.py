from dataclasses import dataclass
from datetime import date

from application.dto.geo import AddressDto
from application.dto.user import UserDto


@dataclass
class CategoryDto:
    id: int
    name: str
    slug: str


@dataclass
class FundingModelDto:
    id: int
    name: str
    slug: str
    description: str | None
    recommended: bool


@dataclass
class CompanyFounderDto:
    name: str
    surname: str
    description: str | None


@dataclass
class CompanyDto:
    id: int
    name: str
    slug: str
    founder: CompanyFounderDto
    country_code: str
    business_id: str
    established_date: date


@dataclass
class CompanyFullDto(CompanyDto):
    address: AddressDto | None = None


@dataclass(frozen=True)
class ProjectStepDto:
    id: int
    name: str
    description: str
    date: date


@dataclass(frozen=True)
class IncubatorDto:
    id: int
    name: str
    description: str


@dataclass(frozen=True)
class AcceleratorDto:
    id: int
    name: str
    description: str


@dataclass(frozen=True)
class CrowdfundingDto:
    id: int
    name: str
    amount: float


@dataclass(frozen=True)
class SocialLinkDto:
    platform: str
    url: str


@dataclass(frozen=True)
class ProjectInvestmentDto:
    id: int
    organization_name: str
    slug: str
    amount: float
    social_links: list[SocialLinkDto]
    phones: list[str]


@dataclass(frozen=True)
class GovernmentGrantDto:
    id: int
    grant_name: str
    grant_name_slug: str
    amount: float
    organization_name: str
    organization_name_slug: str


@dataclass(frozen=True)
class BootstrapDto:
    id: int
    description: str


@dataclass(frozen=True)
class BankLoanDto:
    id: int
    organization_name: str
    amount: float
    terms: str


@dataclass(frozen=True)
class UsefulLinkDto:
    id: int
    name: str
    url: str


@dataclass(frozen=True)
class ProjectDto:
    id: int
    name: str
    slug: str
    goal_descriptioin: str | None
    description: str
    media: list[str | None]
    categories: list[CategoryDto]
    company: CompanyDto
    user: UserDto
    funding_model: FundingModelDto
    goal_sum: float
    current_sum: float
    deadline: date
    stage: str
    status: str
    is_favorite: bool = False


@dataclass(frozen=True)
class ProjectFullDto(ProjectDto):
    file_urls: list[str] | None = None
    steps: list[ProjectStepDto] | None = None
    incubator: IncubatorDto | None = None
    accelerator: AcceleratorDto | None = None
    crowdfunding: CrowdfundingDto | None = None
    investments: list[ProjectInvestmentDto] | None = None
    government_grants: list[GovernmentGrantDto] | None = None
    bootstraps: list[BootstrapDto] | None = None
    bank_loans: list[BankLoanDto] | None = None
    ltv: float | None = None
    arpu: float | None = None
    arppu: float | None = None
    cac: float | None = None
    nps: float | None = None
    roi: float | None = None
    aov: float | None = None
    churn_rate: float | None = None
    retention_rate: float | None = None
    conversion_rate: float | None = None
    useful_links: list[UsefulLinkDto] | None = None

    total_investment_amount: float = 0
