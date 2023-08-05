from datetime import datetime, timedelta

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone

from .manager import AccountManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=100, unique=True)
    fullname = models.CharField(max_length=100, blank=True, null=True)
    role = models.CharField(max_length=100, blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    otp_verified = models.BooleanField(default=False)

    def get_fullname(self):
        '''return the full name of the user'''
        return self.fullname if self.fullname else self.email if self.email else 'Anonymous'  # noqa

    objects = AccountManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.get_fullname()

    class Meta:
        db_table = 'user'
