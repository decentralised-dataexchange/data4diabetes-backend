from django.urls import path
from otp_auth.views import (
    register_user
)

app_name = 'otp_auth'

urlpatterns = [
    path('register/', register_user, name='register_user'),
]
