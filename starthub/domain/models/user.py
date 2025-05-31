from typing import Any

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import EmailValidator, MaxLengthValidator, MinLengthValidator, RegexValidator
from django.db import models
from django.utils import timezone
from domain.constants import (
    CHAR_FIELD_MAX_LENGTH,
    PASSWORD_MAX_LENGTH,
    PASSWORD_MIN_LENGTH,
    PASSWORD_PATTERN,
    USERNAME_MAX_LENGTH,
    USERNAME_MIN_LENGTH,
    USERNAME_PATTERN,
)
from domain.models.base import BaseModel


class UserManager(BaseUserManager["User"]):
    def create_user(
        self,
        email: str,
        username: str,
        password: str | None = None,
        **extra_fields: dict[str, Any],
    ) -> "User":
        if not email:
            raise ValueError("The Email must be set")
        if not username:
            raise ValueError("The Username must be set")
        normalized_email: str = self.normalize_email(email)
        user: "User" = self.model(
            email=normalized_email,
            username=username,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self,
        email: str,
        username: str,
        password: str | None = None,
        **extra_fields: Any,
    ) -> "User":
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self.create_user(email, username, password, **extra_fields)


class User(AbstractBaseUser, BaseModel, PermissionsMixin):
    email = models.CharField(max_length=CHAR_FIELD_MAX_LENGTH, unique=True, validators=[EmailValidator()])
    username = models.CharField(
        max_length=CHAR_FIELD_MAX_LENGTH,
        unique=True,
        validators=[
            RegexValidator(USERNAME_PATTERN),
            MinLengthValidator(USERNAME_MIN_LENGTH),
            MaxLengthValidator(USERNAME_MAX_LENGTH),
        ],
    )
    password = models.CharField(
        max_length=128,
        validators=[
            RegexValidator(PASSWORD_PATTERN),
            MinLengthValidator(PASSWORD_MIN_LENGTH),
            MaxLengthValidator(PASSWORD_MAX_LENGTH),
        ],
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self) -> str:
        return self.username

    def get_short_name(self) -> str:
        return self.username

    def get_full_name(self) -> str:
        return self.username

    class Meta:
        db_table = "users"
        verbose_name = "user"
        verbose_name_plural = "users"
