from dataclasses import dataclass


@dataclass(frozen=True)
class NotificationDto:
    title: str
    message: str
    is_read: bool
