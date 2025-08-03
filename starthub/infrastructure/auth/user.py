from application.dto.auth import AccessPayloadDto, AnonymousPayloadDto
from domain.enums.token import TokenTypeEnum
from domain.value_objects.common import Id
from infrastructure.auth.token import (
    get_access_or_anonymous_payload_dto_from_headers,
    get_access_payload_dto_from_headers,
)
from loguru import logger
from rest_framework.request import Request


def get_user_id_or_none(request: Request) -> Id | None:
    token: AccessPayloadDto | AnonymousPayloadDto = get_access_or_anonymous_payload_dto_from_headers(
        headers=request.headers
    )
    user_id: Id | None = None
    if token.type == TokenTypeEnum.ACCESS:
        user_id = Id(value=int(token.sub))
        return user_id

    logger.debug(f"user_id = {user_id}")
    return None


def get_user_id_or_raises(request: Request) -> Id:
    token: AccessPayloadDto = get_access_payload_dto_from_headers(headers=request.headers)
    user_id: Id = Id(value=int(token.sub))

    logger.debug(f"user_id = {user_id}")
    return user_id
