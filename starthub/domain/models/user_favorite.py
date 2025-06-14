from django.db import models
from domain.models.base import BaseModel


class UserFavorite(BaseModel):
    user = models.ForeignKey("domain.User", on_delete=models.CASCADE)
    project = models.ForeignKey("domain.Project", on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "user_favorites"
        unique_together = ("user", "project")

    def __str__(self) -> str:
        return f"(user_id={self.user_id}, project_id={self.project_id})"
