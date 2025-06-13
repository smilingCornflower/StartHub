from dataclasses import dataclass
from datetime import date


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
    name: str
    slug: str
    founder: CompanyFounderDto
    country_code: str
    business_id: str
    established_date: date


@dataclass
class ProjectDto:
    id: int
    name: str
    slug: str
    description: str
    category: CategoryDto
    company: CompanyDto
    creator_id: int
    funding_model: FundingModelDto
    goal_sum: float
    current_sum: float
    deadline: date
    stage: str
