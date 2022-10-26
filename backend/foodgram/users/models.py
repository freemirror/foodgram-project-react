from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(null=False, max_length=150)
    last_name = models.CharField(null=False, max_length=150)
    email = models.EmailField(_('email address'), max_length=254, unique=True, null=False)
    password = models.CharField(max_length=150)
    is_admin = models.BooleanField(default=False)
