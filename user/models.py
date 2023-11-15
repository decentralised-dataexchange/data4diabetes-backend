import typing
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core.validators import RegexValidator


class UserAccountManager(BaseUserManager):

    def create_superuser(self,
                         username: typing.Union[str, None] = None,
                         mobile_number: typing.Union[str, None] = None,
                         firstname: typing.Union[str, None] = None,
                         lastname: typing.Union[str, None] = None,
                         password: typing.Union[str, None] = None,
                         **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError('Superuser must be assigned to is_staff=True')

        if other_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must be assigned to is_superuser=True')
        user = self.create_user(
            username, mobile_number, firstname, lastname, password, **other_fields)
        user.set_password(password)
        user.save()
        return user

    def create_user(self,
                    username: typing.Union[str, None] = None,
                    mobile_number: typing.Union[str, None] = None,
                    firstname: typing.Union[str, None] = None,
                    lastname: typing.Union[str, None] = None,
                    password: typing.Union[str, None] = None,
                    **other_fields):
        if password is not None:
            user = self.model(username=username,
                              mobile_number=mobile_number,
                              firstname=firstname,
                              lastname=lastname,
                              password=password,
                              **other_fields)
            user.save()
        else:
            user = self.model(username=username,
                              mobile_number=mobile_number,
                              firstname=firstname,
                              lastname=lastname,
                              password=password,
                              **other_fields)
            user.set_unusable_password()
            user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin):

    username = models.CharField(max_length=150, unique=True)
    mobile_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$', message="Please enter a valid mobile number")
    mobile_number = models.CharField(
        validators=[mobile_regex], max_length=17, blank=True, null=True)
    firstname = models.CharField(max_length=20, blank=True, null=True)
    lastname = models.CharField(max_length=512, blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    objects = UserAccountManager()
    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.username or self.mobile_number
