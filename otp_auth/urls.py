from django.urls import path
from otp_auth.views import (
    register_user,
    login_user,
    verify_otp,
    logout_user,
    validate_mobile_number
)

app_name = 'otp_auth'

urlpatterns = [
    path('register/', register_user, name='register_user'),
    path('login/', login_user, name='login_user'),
    path('verify-otp/', verify_otp, name='verify_otp'),
    path('logout/', logout_user, name='logout_user'),
    path('validate-mobile-number/', validate_mobile_number, name='validate_mobile_number'),
]
