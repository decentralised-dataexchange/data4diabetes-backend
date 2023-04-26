from datetime import datetime, timedelta
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.test import TestCase
from unittest.mock import patch
from otp_auth.models import OTP
from otp_auth.user import (
    generate_otp,
    get_user_by_mobile_number,
    is_user_active,
    is_otp_expired,
    send_otp_verification_code
)


class TestUser(TestCase):

    def setUp(self):
        self.User = get_user_model()
        self.user = self.User.objects.create(
            username='+1234567890', is_active=True)

    def test_generate_otp(self):
        self.assertEqual(len(generate_otp(6)), 6)

    def test_get_user_by_mobile_number(self):
        user, is_exists = get_user_by_mobile_number('+1234567890')
        self.assertEqual(user, self.user)
        self.assertTrue(is_exists)

        user, is_exists = get_user_by_mobile_number('invalid_mobile_number')
        self.assertIsNone(user)
        self.assertFalse(is_exists)

    def test_is_user_active(self):
        self.assertTrue(is_user_active(self.user))

        inactive_user = self.User.objects.create(
            username='+0987654321', is_active=False)
        self.assertFalse(is_user_active(inactive_user))

        self.assertFalse(is_user_active(None))

    def test_is_otp_expired(self):
        otp = OTP.objects.create(user=self.user)
        otp_created_time = timezone.now() - timedelta(minutes=15)
        otp.created = otp_created_time
        otp.save()

        # OTP expired
        self.assertTrue(is_otp_expired(otp))

        # OTP not expired
        otp.created = timezone.now() - timedelta(minutes=4)
        otp.save()
        self.assertFalse(is_otp_expired(otp))

    @patch('twilio.rest.Client')
    def test_send_otp_verification_code(self, mock_client):
        User = get_user_model()
        user = User.objects.create(username='1234567890')
        mock_twilio_client = mock_client.return_value
        mock_twilio_client.messages.create.return_value = None
        send_otp_verification_code(user)
        mock_twilio_client.messages.create.assert_called_once()
