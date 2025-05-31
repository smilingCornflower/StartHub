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
class ProjectDto:
    id: int
    name: str
    slug: str
    description: str
    category: CategoryDto
    creator_id: int
    funding_model: FundingModelDto
    goal_sum: float
    current_sum: float
    deadline: date
