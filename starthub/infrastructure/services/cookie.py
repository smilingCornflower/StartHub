from application.ports.cookie_service import AbstractCookieService, CookiesResponseProtocol
from config.settings import CookiesPolicy
from domain.enums.token import TokenNameEnum


class CookieService(AbstractCookieService):
    def remove_access_token_from_cookies(self, response: CookiesResponseProtocol) -> None:
        response.delete_cookie(key=TokenNameEnum.ACCESS_TOKEN)

    def remove_refresh_token_from_cookies(self, response: CookiesResponseProtocol) -> None:
        response.delete_cookie(key=TokenNameEnum.REFRESH_TOKEN)

    def set_refresh_token_to_cookies(self, response: CookiesResponseProtocol, token: str) -> None:
        response.set_cookie(
            key=TokenNameEnum.REFRESH_TOKEN,
            value=token,
            httponly=CookiesPolicy.RefreshToken.HTTPONLY,
            samesite=CookiesPolicy.RefreshToken.SAMESITE,
            secure=CookiesPolicy.RefreshToken.SECURE,
        )


cookie_service = CookieService()
