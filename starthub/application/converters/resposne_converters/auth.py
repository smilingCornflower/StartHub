from application.dto.auth import AccessPayloadDto, AccessTokenDto, TokenPairDto
from domain.value_objects.token import AccessPayload, AccessTokenVo, TokenPairVo


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
        email=access_payload.email,
        iat=access_payload.iat,
        exp=access_payload.exp,
        type=access_payload.type,
    )
