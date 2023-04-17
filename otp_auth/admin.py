from django.contrib import admin
from otp_auth.models import OTP

# Register your models here.
class OTPAdmin(admin.ModelAdmin):
    list_display = ('user', 'created')

admin.site.register(OTP, OTPAdmin)