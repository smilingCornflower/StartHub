from application.dto.auth import AccessPayloadDto, AccessTokenDto, AnonymousPayloadDto, TokenPairDto
from domain.value_objects.auth_management.token import AccessPayload, AccessTokenVo, AnonymousPayload, TokenPairVo


def token_pair_to_dto(token_pair: TokenPairVo) -> TokenPairDto:
    return TokenPairDto(
        access_token=token_pair.access.value,
        refresh_token=token_pair.refresh.value,
    )


def access_token_to_dto(access_token: AccessTokenVo) -> AccessTokenDto:
    return AccessTokenDto(access_token=access_token.value)


def access_payload_to_dto(access_payload: AccessPayload) -> AccessPayloadDto:
    return AccessPayloadDto(
        sub=access_payload.sub,
        roles=access_payload.roles,
        email=access_payload.email,
        first_name=access_payload.first_name,
        last_name=access_payload.last_name,
        iat=access_payload.iat,
        exp=access_payload.exp,
    )


def anonymous_payload_to_dto(anonymous_payload: AnonymousPayload) -> AnonymousPayloadDto:
    return AnonymousPayloadDto(
        sub=anonymous_payload.sub,
        iat=anonymous_payload.iat,
        exp=anonymous_payload.exp,
    )
