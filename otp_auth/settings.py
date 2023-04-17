import os
from django.conf import settings
from rest_framework.settings import APISettings

USER_SETTINGS = getattr(settings, 'OTP_AUTH', None)

DEFAULTS = {
    'TWILIO_FROM_MOBILE_NUMBER': None,
    'TWILIO_ACCOUNT_SID': None,
    'TWILIO_AUTH_TOKEN': None,
    'OTP_MESSAGE_TEMPLATE': 'Use this OTP to securely log in: %s'
}

api_settings = APISettings(USER_SETTINGS, DEFAULTS)
