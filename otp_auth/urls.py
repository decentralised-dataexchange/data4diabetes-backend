from django.urls import path
from otp_auth.views import (
    register_user,
    login_user,
    verify_otp
)

app_name = 'otp_auth'

urlpatterns = [
    path('register/', register_user, name='register_user'),
    path('login/', login_user, name='login_user'),
    path('verify-otp/', verify_otp, name='verify_otp'),
]
