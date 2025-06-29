from enum import StrEnum


class ProjectStatusEnum(StrEnum):
    ACTIVE = "active"
    COMPLETED = "completed"
    DRAFT = "draft"
    UNDER_MODERATION = "under_moderation"
    FUNDRAISING = "fundraising"
    SUSPENDED = "suspended"
    CANCELLED = "cancelled"
