from django.test import SimpleTestCase
from domain.enums.social_links import SocialPlatformEnum
from domain.exceptions.validation import DisallowedSocialLinkException, InvalidSocialLinkException
from domain.value_objects.common import SocialLink
from tests.common.check_raises import check_raises_in_docs


class TestSocialLink(SimpleTestCase):
    def test_valid_link(self):
        platform = SocialPlatformEnum.INSTAGRAM
        link = "https://instagram.com/user"
        social_link = SocialLink(platform=platform, link=link)

        self.assertEqual(social_link.platform, platform)
        self.assertEqual(social_link.link, link)

    def test_unknown_platform(self):
        exception = DisallowedSocialLinkException
        with self.assertRaises(exception):
            SocialLink(platform="unknown", link="https://example.com")
        check_raises_in_docs(SocialLink.validate_social_link, exception)

    def test_invalid_link_format(self):
        exception = InvalidSocialLinkException
        with self.assertRaises(exception):
            SocialLink(platform=SocialPlatformEnum.INSTAGRAM, link="invalid-link")
        check_raises_in_docs(SocialLink.validate_social_link, exception)
