from uuid import uuid4

from domain.models.user_management.user import User


def get_test_user():
    user, _ = User.objects.get_or_create(email="test@example.com", password="Password1234!")
    return user


def get_random_user():
    user, _ = User.objects.get_or_create(email=f"{uuid4().hex}@example.com", password="Password1234!")
    return user
