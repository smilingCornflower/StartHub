from enum import StrEnum


class ActionEnum(StrEnum):
    ADD = "add"
    VIEW = "view"
    CHANGE = "change"
    DELETE = "DELETE"
    MANAGE = "manage"  # add, view, change and delete


class ScopeEnum(StrEnum):
    ANY = "any"
    OWN = "own"
