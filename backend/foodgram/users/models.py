from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    first_name = models.CharField(null=False, max_length=30)
    last_name = models.CharField(null=False, max_length=50)
    email = models.EmailField(_('email address'), max_length=254, unique=True)
    is_admin = models.BooleanField(default=False)