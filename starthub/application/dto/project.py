from dataclasses import dataclass
from datetime import date

from application.dto.geo import AddressDto


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
class ProjectDto:
    id: int
    name: str
    slug: str
    goal_descriptioin: str | None
    description: str
    images: list[str]
    categories: list[CategoryDto]
    company: CompanyDto
    creator_id: int
    funding_model: FundingModelDto
    goal_sum: float
    current_sum: float
    deadline: date
    stage: str
    status: str
    is_favorite: bool = False


@dataclass(frozen=True)
class ProjectFullDto(ProjectDto):
    steps: list[ProjectStepDto] | None = None
    incubator: IncubatorDto | None = None
