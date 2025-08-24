from django.db import models
from domain.constants import CHAR_FIELD_MAX_LENGTH, CHAR_FIELD_SHORT_LENGTH
from domain.models.base import BaseModel


class UserMessage(BaseModel):
    user = models.ForeignKey("domain.User", on_delete=models.CASCADE, related_name="messages")
    first_name = models.CharField(max_length=CHAR_FIELD_SHORT_LENGTH)
    last_name = models.CharField(max_length=CHAR_FIELD_SHORT_LENGTH)
    email = models.CharField(max_length=CHAR_FIELD_MAX_LENGTH)
    phone = models.CharField(max_length=CHAR_FIELD_SHORT_LENGTH)
    topic = models.CharField(max_length=CHAR_FIELD_MAX_LENGTH)
    content = models.TextField()

    class Meta:
        db_table = "user_messages"

    def __str__(self) -> str:
        return f"{self.email} | {self.topic[:50]}..."

    @classmethod
    def get_permission_key(cls) -> str:
        return "user_message"
