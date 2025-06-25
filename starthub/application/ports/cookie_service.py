from abc import ABC, abstractmethod
from typing import Any, Protocol


class CookiesResponseProtocol(Protocol):
    def set_cookie(self, key: str, value: str, httponly: bool, samesite: str, secure: bool, **kwargs: Any) -> None:
        pass

    def delete_cookie(self, key: str, **kwargs: Any) -> None:
        pass


class AbstractCookieService(ABC):
    @abstractmethod
    def set_access_token_to_cookies(self, response: CookiesResponseProtocol, token: str) -> None:
        pass

    @abstractmethod
    def set_refresh_token_to_cookies(self, response: CookiesResponseProtocol, token: str) -> None:
        pass

    @abstractmethod
    def remove_access_token_from_cookies(self, response: CookiesResponseProtocol) -> None:
        pass

    @abstractmethod
    def remove_refresh_token_from_cookies(self, response: CookiesResponseProtocol) -> None:
        pass
