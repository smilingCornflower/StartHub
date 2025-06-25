from application.ports.cookie_service import AbstractCookieService, CookiesResponseProtocol
from domain.enums.token import TokenNameEnum


class CookieService(AbstractCookieService):
    def remove_access_token_from_cookies(self, response: CookiesResponseProtocol) -> None:
        response.delete_cookie(key=TokenNameEnum.ACCESS_TOKEN)

    def remove_refresh_token_from_cookies(self, response: CookiesResponseProtocol) -> None:
        response.delete_cookie(key=TokenNameEnum.REFRESH_TOKEN)

    def set_access_token_to_cookies(self, response: CookiesResponseProtocol, token: str) -> None:
        response.set_cookie(
            key=TokenNameEnum.ACCESS_TOKEN,
            value=token,
            httponly=True,
            samesite="Lax",
            secure=False,
        )

    def set_refresh_token_to_cookies(self, response: CookiesResponseProtocol, token: str) -> None:
        response.set_cookie(
            key=TokenNameEnum.REFRESH_TOKEN,
            value=token,
            httponly=True,
            samesite="Lax",
            secure=False,
        )


cookie_service = CookieService()
