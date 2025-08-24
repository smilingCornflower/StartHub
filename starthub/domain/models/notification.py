from domain.constants import CHAR_FIELD_MAX_LENGTH
from domain.models.base import BaseModel
from django.db import models


class Notification(BaseModel):
    user = models.ForeignKey("domain.User", on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=CHAR_FIELD_MAX_LENGTH)
    message = models.TextField()

    is_read = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Notification for {self.user.email}: {self.title}"

    @classmethod
    def get_permission_key(cls) -> str:
        return "notification"
