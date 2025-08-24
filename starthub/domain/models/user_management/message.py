from django.db import models

from domain.constants import CHAR_FIELD_SHORT_LENGTH, CHAR_FIELD_MAX_LENGTH
from domain.models.base import BaseModel


class UserMessage(BaseModel):
    first_name = models.CharField(max_length=CHAR_FIELD_SHORT_LENGTH)
    last_name = models.CharField(max_length=CHAR_FIELD_SHORT_LENGTH)
    email = models.CharField(max_length=CHAR_FIELD_MAX_LENGTH)
    phone = models.CharField(max_length=CHAR_FIELD_SHORT_LENGTH)
    topic = models.CharField(max_length=CHAR_FIELD_MAX_LENGTH)
    message = models.TextField()

    class Meta:
        db_table = "user_messages"

    def __str__(self) -> str:
        return f"{self.email} | {self.topic[:50]}..."

    @classmethod
    def get_permission_key(cls) -> str:
        return "user_message"
