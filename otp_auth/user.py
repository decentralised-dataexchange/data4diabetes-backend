import typing
import string
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractBaseUser
from django.utils import timezone
from django.utils.crypto import get_random_string
from otp_auth.settings import api_settings, OTP_AUTH_OTP_EXPIRY_IN_MINUTES
from otp_auth.models import OTP
from hashlib import sha256
from datetime import timedelta
from rest_framework.authtoken.models import Token


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


def get_otp_by_otp_hash(otp_to_be_verified):
    """Check if OTP instance is present or not"""
    try:
       otp = OTP.objects.get(otp_hash=sha256(otp_to_be_verified.encode('utf-8')).hexdigest())
       return otp, True
    except OTP.DoesNotExist:
        return None, False
    

def is_otp_expired(otp: OTP) -> bool:
    """Check if OTP has expired"""
    otp_created_time = otp.created
    current_time = timezone.now()
    otp_expiry_time = otp_created_time + timedelta(minutes=OTP_AUTH_OTP_EXPIRY_IN_MINUTES)
    if current_time >= otp_expiry_time:
        return True
    else:
        return False
    
    
def issue_token(user) -> Token:
    """Create Token for the user"""
    token = Token.objects.create(user=user)
    return token


def delete_token(user: AbstractBaseUser):
    """Delete Token of the user"""
    user.auth_token.delete()
    user.save()
    return
