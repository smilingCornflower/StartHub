from enum import StrEnum


class SocialPlatform(StrEnum):
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


_PLATFORM_PATTERNS: dict[SocialPlatform, str] = {
    SocialPlatform.FACEBOOK: r"^(?:https?:)?\/\/(?:www\.)?(?:facebook|fb)\.com\/.*$",
    SocialPlatform.INSTAGRAM: r"^(?:https?:)?\/\/(?:www\.)?(?:instagram\.com|instagr\.am)\/.*$",
    SocialPlatform.TWITTER: r"^(?:https?:)?\/\/(?:[\w\-]+\.)?twitter\.com\/.*$",
    SocialPlatform.LINKEDIN: r"^(?:https?:)?\/\/(?:[\w\-]+\.)?linkedin\.com\/.*$",
    SocialPlatform.VK: r"^(?:https?:)?\/\/(?:www\.)?vk\.com\/.*$",
    SocialPlatform.TELEGRAM: r"^(?:https?:)?\/\/(?:t(?:elegram)?\.me|telegram\.org)\/.*$",
    SocialPlatform.YOUTUBE: r"^(?:https?:)?\/\/(?:[\w\-]+\.)?youtube\.com\/.*$",
    SocialPlatform.TIKTOK: r"^(?:https?:)?\/\/(?:www\.)?tiktok\.com\/.*$",
}
