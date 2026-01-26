import binascii
import os
from datetime import timedelta

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class AnonymousLogin(models.Model):
    token = models.CharField(_("token"), max_length=64, db_index=True, unique=True)
    created = models.DateTimeField(_("created"), auto_now_add=True)
    request_data = models.JSONField(default=dict)
    expiration_datetime = models.DateTimeField(
        _("expiration datetime"),
        null=True,
        default=None,
    )

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = self.generate_token()

        if not self.expiration_datetime:
            self.expiration_datetime = self.set_default_expiration_datetime()
        return super().save(*args, **kwargs)

    @staticmethod
    def generate_token():
        return binascii.hexlify(os.urandom(32)).decode()

    @staticmethod
    def set_default_expiration_datetime():
        default_expiration = getattr(settings, "ANONYMOUS_LOGIN_EXPIRATION", None)
        if default_expiration:
            return timezone.now() + timedelta(minutes=default_expiration)


class AnonymousLoginUserMixin:
    @property
    def is_anonymous_login(self):
        return AnonymousLogin.objects.filter(token=self.username).exists()

    @property
    def anonymous_login(self):
        """
        Returns the "longest" (with the latest expiration) AnonymousLogin element matching the user's username
        """
        return AnonymousLogin.objects.filter(token=self.username).order_by("-expiration_datetime").first()
