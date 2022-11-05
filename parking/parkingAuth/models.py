from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        max_length=100, unique=True, blank=True, null=True, validators=[username_validator])
    email = models.EmailField(unique=True, blank=True, null=True)
    first_name = models.CharField(max_length=150, blank=True, null=True)
    last_name = models.CharField(max_length=150, blank=True, null=True)
    phone = models.CharField(unique=True, max_length=12)
    date_joined = models.DateTimeField(auto_now_add=True)
    # TODO: в бою должна быть активация
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'phone'
    EMAIL_FIELD = 'email'
