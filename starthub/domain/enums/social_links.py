from enum import StrEnum


class SocialPlatformEnum(StrEnum):
    FACEBOOK = "facebook"
    INSTAGRAM = "instagram"
    TWITTER = "twitter"
    LINKEDIN = "linkedin"
    VK = "vk"
    TELEGRAM = "telegram"
    YOUTUBE = "youtube"
    TIKTOK = "tiktok"

    @property
    def pattern(self) -> str:
        return _PLATFORM_PATTERNS[self]


_PLATFORM_PATTERNS: dict[SocialPlatformEnum, str] = {
    SocialPlatformEnum.FACEBOOK: r"^(?:https?:)?\/\/(?:www\.)?(?:facebook|fb)\.com\/.*$",
    SocialPlatformEnum.INSTAGRAM: r"^(?:https?:)?\/\/(?:www\.)?(?:instagram\.com|instagr\.am)\/.*$",
    SocialPlatformEnum.TWITTER: r"^(?:https?:)?\/\/(?:[\w\-]+\.)?twitter\.com\/.*$",
    SocialPlatformEnum.LINKEDIN: r"^(?:https?:)?\/\/(?:[\w\-]+\.)?linkedin\.com\/.*$",
    SocialPlatformEnum.VK: r"^(?:https?:)?\/\/(?:www\.)?vk\.com\/.*$",
    SocialPlatformEnum.TELEGRAM: r"^(?:https?:)?\/\/(?:t(?:elegram)?\.me|telegram\.org)\/.*$",
    SocialPlatformEnum.YOUTUBE: r"^(?:https?:)?\/\/(?:[\w\-]+\.)?youtube\.com\/.*$",
    SocialPlatformEnum.TIKTOK: r"^(?:https?:)?\/\/(?:www\.)?tiktok\.com\/.*$",
}
