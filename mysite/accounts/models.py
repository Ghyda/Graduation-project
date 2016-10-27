from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractBaseUser

class User(AbstractBaseUser):
    """
    Custom user class.
    """
    username = models.CharField('Username', unique=True, db_index=True, max_length=40)
    joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'

    def __unicode__(self):
        return self.username
