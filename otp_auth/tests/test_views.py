from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate
from django.test import TestCase
from unittest.mock import patch
from hashlib import sha256
from django.contrib.auth import get_user_model
from otp_auth.views import (
    register_user, login_user, verify_otp, logout_user
)
from rest_framework.authtoken.models import Token

factory = APIRequestFactory()
User = get_user_model()


class TestUser(TestCase):

    @patch('twilio.rest.Client')
    def test_register_user(self, mock_client):
        mobile_number = "1234567890"
        request_data = {
            "firstname": "John",
            "lastname": "Doe",
            "mobile_number": mobile_number,
        }
        request = factory.post(
            '/register_user/', data=request_data, format='json')
        response = register_user(request)
        assert response.status_code == status.HTTP_201_CREATED

        # Ensure the OTP was sent
        user = User.objects.get(mobile_number=mobile_number)
        assert user.otp_set.exists()

    @patch('twilio.rest.Client')
    def test_login_user(self, mock_client):
        mobile_number = "1234567890"
        user = User.objects.create_user(
            username=mobile_number,
            mobile_number=mobile_number,
            is_active=True
        )
        request_data = {"mobile_number": mobile_number}
        request = factory.post(
            '/login_user/', data=request_data, format='json')
        response = login_user(request)
        assert response.status_code == status.HTTP_200_OK

        # Ensure the OTP was sent
        user.refresh_from_db()
        assert user.otp_set.exists()

    def test_verify_otp(self):
        mobile_number = "1234567890"
        user = User.objects.create_user(
            username=mobile_number,
            mobile_number=mobile_number
        )

        raw_otp = "666666"
        raw_otp_hash = sha256(raw_otp.encode('utf-8')).hexdigest()
        user.otp_set.create(otp_hash=raw_otp_hash)

        request_data = {"otp": raw_otp}

        request = factory.post(
            '/verify_otp/', data=request_data, format='json')

        response = verify_otp(request)
        assert response.status_code == status.HTTP_200_OK

        # Ensure the user is now active and the OTP is deleted
        user.refresh_from_db()

        assert user.is_active is True
        assert not user.otp_set.exists()
        assert 'data' in response.data
        assert 'token' in response.data['data'].keys()

    def test_logout_user(self):
        mobile_number = "1234567890"
        user = User.objects.create_user(
            username=mobile_number,
            mobile_number=mobile_number
        )

        token, _ = Token.objects.get_or_create(user=user)
        token = token.key

        request = factory.post(
            '/logout_user/', HTTP_AUTHORIZATION=f'Token {token}')
        force_authenticate(request, user=user)
        response = logout_user(request)
        assert response.status_code == status.HTTP_204_NO_CONTENT

        # Ensure the token was deleted
        user.refresh_from_db()
        with self.assertRaises(User.auth_token.RelatedObjectDoesNotExist):
            user.auth_token
