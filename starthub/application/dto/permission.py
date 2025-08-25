from dataclasses import dataclass


@dataclass(frozen=True)
class PermissionDto:
    id: int
    name: str
