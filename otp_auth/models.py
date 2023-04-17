from django.db import models
from django.conf import settings


class OTP(models.Model):
    """One time passcode model"""
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name=None, on_delete=models.CASCADE)
    otp_hash = models.CharField(max_length=128)

    def __str__(self):
        return self.user.username
