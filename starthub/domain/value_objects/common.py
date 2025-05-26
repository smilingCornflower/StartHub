from dataclasses import dataclass


@dataclass(frozen=True)
class Id:
    value: int


@dataclass(frozen=True)
class Slug:
    value: str
