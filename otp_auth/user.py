import typing
import string
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractBaseUser
from django.utils.crypto import get_random_string
from otp_auth.settings import api_settings
from otp_auth.models import OTP
from hashlib import sha256


def generate_otp(max_length: int):
    """
    Generate an OTP of max length
    """
    return get_random_string(length=max_length, allowed_chars=string.digits)


def get_user_by_mobile_number(mobile_number: str) -> typing.Tuple[AbstractBaseUser, bool]:
    """Query `User` instance by mobile number and return the `User` instance, existence boolean"""
    User = get_user_model()
    try:
        user = User.objects.get(username=mobile_number)
        return user, True
    except User.DoesNotExist:
        return None, False


def is_user_active(user: AbstractBaseUser) -> bool:
    """Check if `User` instance is active or not"""
    return user.is_active if user else False


def send_otp_verification_code(user: AbstractBaseUser) -> None:
    """Send OTP verification code to the mobile number of the user"""
    from twilio.rest import Client
    twilio_client = Client(api_settings.TWILIO_ACCOUNT_SID,
                           api_settings.TWILIO_AUTH_TOKEN)

    otp = generate_otp(6)

    # Save OTP to database.
    OTP.objects.create(user=user, otp_hash=sha256(
        otp.encode('utf-8')).hexdigest())

    twilio_client.messages.create(
        body=api_settings.OTP_MESSAGE_TEMPLATE % otp,
        to=user.mobile_number,
        from_=api_settings.TWILIO_FROM_MOBILE_NUMBER
    )
