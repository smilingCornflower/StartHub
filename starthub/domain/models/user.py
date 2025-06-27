from typing import Any

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import EmailValidator, MaxLengthValidator, MinLengthValidator, RegexValidator
from django.db import models
from django.utils import timezone
from domain.constants import (
    CHAR_FIELD_MAX_LENGTH,
    CHAR_FIELD_SHORT_LENGTH,
    DESCRIPTION_MAX_LENGTH,
    NAME_PATTERN,
    PASSWORD_MAX_LENGTH,
    PASSWORD_MIN_LENGTH,
    PASSWORD_PATTERN,
)
from domain.models.base import BaseModel
from domain.models.role import get_default_role


class UserManager(BaseUserManager["User"]):
    def create_user(
        self,
        email: str | None,
        first_name: str | None = None,
        last_name: str | None = None,
        password: str | None = None,
        **extra_fields: dict[str, Any],
    ) -> "User":
        """:raises ValueError:"""
        if not email:
            raise ValueError("Email must be set.")
        normalized_email: str = self.normalize_email(email)
        if first_name and last_name:
            user = self.model(
                email=normalized_email,
                first_name=first_name,
                last_name=last_name,
                **extra_fields,
            )
        else:
            user = self.model(
                email=normalized_email,
                **extra_fields,
            )
        user.set_password(password)
        user.save(using=self._db)
        self._assign_default_role(user)
        return user

    def _assign_default_role(self, user: "User") -> None:
        default_role = get_default_role()
        user.roles.add(default_role)

    def create_superuser(
        self,
        email: str,
        first_name: str,
        last_name: str,
        password: str | None = None,
        **extra_fields: Any,
    ) -> "User":
        """:raises ValueError:"""
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self.create_user(
            email=email, first_name=first_name, last_name=last_name, password=password, **extra_fields
        )


class User(AbstractBaseUser, BaseModel, PermissionsMixin):
    email = models.CharField(max_length=CHAR_FIELD_MAX_LENGTH, unique=True, validators=[EmailValidator()])
    first_name = models.CharField(
        max_length=CHAR_FIELD_SHORT_LENGTH, validators=[RegexValidator(NAME_PATTERN)], default="default first name"
    )
    last_name = models.CharField(
        max_length=CHAR_FIELD_SHORT_LENGTH, validators=[RegexValidator(NAME_PATTERN)], default="default last name"
    )
    password = models.CharField(
        max_length=128,
        validators=[
            RegexValidator(PASSWORD_PATTERN),
            MinLengthValidator(PASSWORD_MIN_LENGTH),
            MaxLengthValidator(PASSWORD_MAX_LENGTH),
        ],
    )
    description = models.CharField(max_length=DESCRIPTION_MAX_LENGTH, default="", blank=True)
    roles = models.ManyToManyField("domain.Role", default=get_default_role, related_name="users")

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    picture = models.CharField(max_length=CHAR_FIELD_MAX_LENGTH, blank=True, null=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    def __str__(self) -> str:
        return self.first_name

    def get_short_name(self) -> str:
        return self.first_name

    def get_full_name(self) -> str:
        return self.first_name + " " + self.last_name

    class Meta:
        db_table = "users"
        verbose_name = "user"
        verbose_name_plural = "users"

    @classmethod
    def get_permission_key(cls) -> str:
        return "user"
