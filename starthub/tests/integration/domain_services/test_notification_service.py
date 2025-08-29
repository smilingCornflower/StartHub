from application.builders.domain_service.notification import NotificationServiceBuilder
from django.test import TestCase
from domain.exceptions.permissions import ViewDeniedPermissionException
from domain.models.notification import Notification
from domain.value_objects.common import Id
from domain.value_objects.notification import NotificationCreatePayload, NotificationMessage, NotificationTitle
from tests.common.builders import get_random_user, get_test_user


class TestNotificationService(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = get_test_user()
        cls.other_user = get_random_user()
        cls.notification_title = "Title"
        cls.notification_message = "Message"

    def setUp(self):
        self.service = NotificationServiceBuilder.create_service()

    def _get_create_payload(self):
        """Create notification payload with test data"""
        return NotificationCreatePayload(
            user_id=Id(value=self.user.id),
            title=NotificationTitle(value=self.notification_title),
            message=NotificationMessage(value=self.notification_message),
        )

    def test_create_notification_successfully(self):
        """Test successful notification creation"""
        self.service.create(payload=self._get_create_payload())

        notification = Notification.objects.filter(user_id=self.user.id).first()

        self.assertEqual(notification.user.email, self.user.email)
        self.assertEqual(notification.title, self.notification_title)
        self.assertEqual(notification.message, self.notification_message)

    def test_mark_notification_as_read(self):
        """Test marking notification as read"""
        notification = self.service.create(payload=self._get_create_payload())

        self.assertFalse(notification.is_read)

        self.service.mark_as_read(notifications=[notification])

        updated_notification = Notification.objects.get(id=notification.id)
        self.assertTrue(updated_notification.is_read)

    def test_check_can_user_read_own_notifications(self):
        """Test user can read their own notifications"""
        self.service.check_can_user_read_notification(caller_user=self.user, target_user=self.user)

    def test_check_cannot_read_other_user_notifications(self):
        """Test user cannot read other user's notifications"""
        with self.assertRaises(ViewDeniedPermissionException):
            self.service.check_can_user_read_notification(caller_user=self.other_user, target_user=self.user)
