from django.db import models
from domain.constants import CHAR_FIELD_MAX_LENGTH
from domain.models.base import BaseModel


class ProjectBankLoan(BaseModel):
    project = models.ForeignKey("domain.Project", on_delete=models.CASCADE, related_name="bank_loans")
    organization_name = models.CharField(max_length=CHAR_FIELD_MAX_LENGTH)
    amount = models.FloatField()
    terms = models.TextField()

    class Meta:
        db_table = "bank_loans"

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(project_id{self.project.id}, amount={self.amount})"

    @classmethod
    def get_permission_key(cls) -> str:
        return "bank_loan"
