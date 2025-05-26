from dataclasses import dataclass
from datetime import date

from domain.ports.payload import AbstractCreatePayload, AbstractUpdatePayload
from domain.value_objects.common import Id


@dataclass
class ProjectCreatePayload(AbstractCreatePayload):
    name: str
    description: str
    category_id: Id
    creator_id: Id
    funding_model_id: Id
    goal_sum: float
    deadline: date
    team_ids: list[Id]


@dataclass
class ProjectUpdatePayload(AbstractUpdatePayload):
    id_: Id
    name: str | None
    description: str | None
    category_id: Id | None
    funding_model_id: Id | None
    goal_sum: float | None
    deadline: date | None
    add_team_ids: list[Id] | None
    remove_team_ids: list[Id] | None
