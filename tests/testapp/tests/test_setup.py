from django.apps import apps
from django.conf import settings
from django.test import SimpleTestCase

from drf_anonymous_login.models import AnonymousLogin
from testapp.models import PrivateModel, PublicModel


class TestSetup(SimpleTestCase):
    def test_installed_apps(self):
        self.assertIn("drf_anonymous_login", settings.INSTALLED_APPS)

    def test_models(self):
        self.assertIs(
            apps.get_model("drf_anonymous_login", "AnonymousLogin"),
            AnonymousLogin,
        )
        self.assertIs(apps.get_model("testapp", "PublicModel"), PublicModel)
        self.assertIs(apps.get_model("testapp", "PrivateModel"), PrivateModel)
