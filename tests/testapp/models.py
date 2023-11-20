from django.contrib.auth.models import AbstractUser
from django.db import models

from drf_anonymous_login.models import AnonymousLoginUserMixin


class PublicModel(models.Model):
    """
    Public model that is visible to anyone (no login required)
    """

    name = models.CharField(max_length=50, primary_key=True)


class PrivateModel(models.Model):
    """
    Private model that requires valid login to be shown
    """

    name = models.CharField(max_length=50, primary_key=True)


class User(AnonymousLoginUserMixin, AbstractUser):
    pass
