import binascii
import os

from django.db import models
from django.utils.translation import gettext_lazy as _


class AnonymousLogin(models.Model):
    token = models.CharField(_("token"), max_length=64, db_index=True, unique=True)
    created = models.DateTimeField(_("created"), auto_now_add=True)
    request_data = models.JSONField(default=dict)
    expiration_datetime = models.DateTimeField(
        _("expiration datetime"), null=True, default=None
    )

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = self.generate_token()
        return super().save(*args, **kwargs)

    @staticmethod
    def generate_token():
        return binascii.hexlify(os.urandom(32)).decode()
