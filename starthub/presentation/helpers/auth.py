from application.services.gateway import gateway
from domain.models.user_management.user import User
from domain.value_objects.auth_management.token import AccessTokenVo, AnonymousTokenVo
from domain.value_objects.user_management.anonymous import AnonymousUser
from presentation.request_converters.user_management.auth import (
    request_to_access_or_anonymous_token,
    request_to_access_token,
)
from rest_framework.request import Request


def get_authenticated_user_from_request(request: Request) -> User:
    token: AccessTokenVo = request_to_access_token(request=request)
    user: User = gateway.auth_app_service.get_authenticated_user(token=token)
    return user


def get_authenticated_or_anonymous_user_from_request(request: Request) -> User | AnonymousUser:
    token: AccessTokenVo | AnonymousTokenVo = request_to_access_or_anonymous_token(request=request)
    user: User | AnonymousUser = gateway.auth_app_service.get_authenticated_or_anonymous_user(token=token)
    return user
