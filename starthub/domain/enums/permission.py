from enum import StrEnum


class ActionEnum(StrEnum):
    ADD = "add"
    VIEW = "view"
    CHANGE = "change"
    DELETE = "delete"


class ScopeEnum(StrEnum):
    ANY = "any"
    OWN = "own"
