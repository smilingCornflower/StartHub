from django.contrib import admin
from django_stubs_ext import monkeypatch
from domain.models.user import User

monkeypatch()


@admin.register(User)
class UserAdmin(admin.ModelAdmin[User]):
    pass
