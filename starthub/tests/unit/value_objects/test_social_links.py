import re

from django.test import SimpleTestCase
from domain.enums.social_links import SocialPlatform


class SocialPlatformPatternTests(SimpleTestCase):
    def _test_urls(self, platform: SocialPlatform, valid_urls: list[str], invalid_urls: list[str]) -> None:
        pattern = re.compile(platform.pattern)
        for url in valid_urls:
            with self.subTest(valid_url=url):
                self.assertTrue(
                    pattern.fullmatch(url),
                    f"URL '{url}' should be valid for {platform.value}, but regex did not match it.",
                )

        for url in invalid_urls:
            with self.subTest(invalid_url=url):
                self.assertIsNone(
                    pattern.fullmatch(url),
                    f"URL '{url}' should be invalid for {platform.value}, but regex matched it.",
                )

    def test_facebook_pattern(self) -> None:
        valid = [
            "https://facebook.com/user",
            "http://facebook.com/user",
            "https://www.facebook.com/user",
            "http://www.facebook.com/user",
            "https://fb.com/user",
            "http://fb.com/user/profile",
        ]
        invalid = [
            "https://fakefacebook.com/user",
            "https://facebook.org/user",
            "facebook.com/user",
            "https://facebook.com",
        ]
        self._test_urls(SocialPlatform.FACEBOOK, valid, invalid)

    def test_instagram_pattern(self) -> None:
        valid = [
            "https://instagram.com/user",
            "http://instagram.com/user",
            "https://www.instagram.com/user",
            "https://instagr.am/user",
            "http://instagr.am/user/profile",
        ]
        invalid = [
            "https://fakeinstagram.com/user",
            "https://instagram.net/user",
            "instagram.com/user",
            "https://instagram.com",
        ]
        self._test_urls(SocialPlatform.INSTAGRAM, valid, invalid)

    def test_twitter_pattern(self) -> None:
        valid = [
            "https://twitter.com/user",
            "http://twitter.com/user",
            "https://subdomain.twitter.com/user",
            "http://another.twitter.com/user/profile",
        ]
        invalid = [
            "https://faketwitter.com/user",
            "https://twitter.org/user",
            "twitter.com/user",
            "https://twitter.com",
        ]
        self._test_urls(SocialPlatform.TWITTER, valid, invalid)

    def test_linkedin_pattern(self) -> None:
        valid = [
            "https://linkedin.com/user",
            "http://linkedin.com/user",
            "https://subdomain.linkedin.com/user",
            "http://another.linkedin.com/user/profile",
        ]
        invalid = [
            "https://fakelinkedin.com/user",
            "https://linkedin.org/user",
            "linkedin.com/user",
            "https://linkedin.com",
        ]
        self._test_urls(SocialPlatform.LINKEDIN, valid, invalid)

    def test_vk_pattern(self) -> None:
        valid = [
            "https://vk.com/user",
            "http://vk.com/user",
            "https://www.vk.com/user",
            "http://www.vk.com/user/profile",
        ]
        invalid = [
            "https://fakevk.com/user",
            "https://vk.org/user",
            "vk.com/user",
            "https://vk.com",
        ]
        self._test_urls(SocialPlatform.VK, valid, invalid)

    def test_telegram_pattern(self) -> None:
        valid = [
            "https://t.me/user",
            "http://telegram.me/user",
            "https://telegram.org/user",
            "http://t.me/user/profile",
        ]
        invalid = [
            "https://faketelegram.com/user",
            "https://telegram.net/user",
            "t.me/user",
            "https://telegram.org",
        ]
        self._test_urls(SocialPlatform.TELEGRAM, valid, invalid)

    def test_youtube_pattern(self) -> None:
        valid = [
            "https://youtube.com/user",
            "http://youtube.com/user",
            "https://subdomain.youtube.com/user",
            "http://another.youtube.com/user/profile",
        ]
        invalid = [
            "https://fakeyoutube.com/user",
            "https://youtube.org/user",
            "youtube.com/user",
            "https://youtube.com",
        ]
        self._test_urls(SocialPlatform.YOUTUBE, valid, invalid)

    def test_tiktok_pattern(self) -> None:
        valid = [
            "https://tiktok.com/user",
            "http://tiktok.com/user",
            "https://www.tiktok.com/user",
            "http://www.tiktok.com/user/profile",
        ]
        invalid = [
            "https://faketiktok.com/user",
            "https://tiktok.org/user",
            "tiktok.com/user",
            "https://tiktok.com",
        ]
        self._test_urls(SocialPlatform.TIKTOK, valid, invalid)
