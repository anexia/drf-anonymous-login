from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_403_FORBIDDEN

from drf_anonymous_login.authentication import AUTH_HEADER, AUTH_KEYWORD
from drf_anonymous_login.management.commands.cleanup_tokens import Command
from drf_anonymous_login.models import AnonymousLogin
from testapp.models import PrivateModel, PublicModel, User


class TestApi(TestCase):
    def setUp(self):
        super().setUp()
        self.anonymous_login = AnonymousLogin.objects.create(request_data={})
        PublicModel.objects.create(name="public model")
        PrivateModel.objects.create(name="private model")

    def login_header(self):
        return {AUTH_HEADER: f"{AUTH_KEYWORD} {self.anonymous_login.token}"}

    def test_no_default_expiration_datetime(self):
        self.assertIsNone(self.anonymous_login.expiration_datetime)

    def test_default_expiration_datetime(self):
        with self.settings(ANONYMOUS_LOGIN_EXPIRATION=15):
            today = timezone.now()
            self.anonymous_login = AnonymousLogin.objects.create(request_data={})
            self.assertIsNotNone(self.anonymous_login.expiration_datetime)
            self.assertGreater(self.anonymous_login.expiration_datetime, today)
            self.assertLess(
                self.anonymous_login.expiration_datetime,
                today + timedelta(minutes=16),
            )

    def test_no_login(self):
        """
        Assert that token is required only for protected viewsets (with AnonymousLoginAuthenticationModelViewSet),
        not for public ones
        :return:
        """
        # make sure public model can be accessed by anyone
        url = reverse("publicmodel-list")
        response = self.client.get(url)
        self.assertEqual(HTTP_200_OK, response.status_code, response.content)

        # make sure private model can not be accessed by anyone
        url = reverse("privatemodel-list")
        response = self.client.get(url)
        self.assertEqual(HTTP_403_FORBIDDEN, response.status_code, response.content)

    def test_anonymous_login_token(self):
        """
        Assert that token allows access
        :return:
        """
        url = reverse("privatemodel-list")
        response = self.client.get(url, **self.login_header())
        self.assertEqual(HTTP_200_OK, response.status_code, response.content)

    def test_anonymous_login_token_invalid(self):
        """
        Assert that an invalid token does not allow access
        :return:
        """
        url = reverse("privatemodel-list")
        response = self.client.get(
            url,
            **{AUTH_HEADER: "{} {}".format(AUTH_KEYWORD, "invalid_token")},
        )
        self.assertEqual(HTTP_403_FORBIDDEN, response.status_code, response.content)
        self.assertEqual(str(response.data["detail"]), "Invalid authentication token")

    def test_anonymous_login_token_expired(self):
        """
        Assert that an expired token does not allow access any more
        :return:
        """
        self.anonymous_login.expiration_datetime = timezone.now() - timedelta(days=2)
        self.anonymous_login.save()
        url = reverse("privatemodel-list")
        response = self.client.get(url, **self.login_header())
        self.assertEqual(HTTP_403_FORBIDDEN, response.status_code, response.content)
        self.assertEqual(str(response.data["detail"]), "Expired authentication token")

    def test_anonymous_login_token_cleanup(self):
        """
        Assert that only an expired token gets deleted from the clean command
        :return:
        """
        self.assertEqual(AnonymousLogin.objects.count(), 1)

        cleanup_tokens = Command()

        # make sure cleanup does nothing
        cleanup_tokens.handle_tick()
        self.assertEqual(AnonymousLogin.objects.count(), 1)

        # expire the token
        self.anonymous_login.expiration_datetime = timezone.now() - timedelta(days=2)
        self.anonymous_login.save()

        # make sure the token gets deleted
        cleanup_tokens.handle_tick()
        self.assertEqual(AnonymousLogin.objects.count(), 0)

    def test_user_is_anonymous_login(self):
        """
        Assert that User is correctly identified as AnonymousLogin
        :return:
        """
        user = User.objects.create(
            username=self.anonymous_login.token,
            password="password",
        )
        self.assertTrue(user.is_anonymous_login)

    def test_user_is_not_anonymous_login(self):
        """
        Assert that User is correctly identified as no AnonymousLogin
        :return:
        """
        user = User.objects.create(username="user", password="password")
        self.assertFalse(user.is_anonymous_login)

    def test_user_get_anonymous_login(self):
        """
        Assert that User can access their AnonymousLogin
        :return:
        """
        user = User.objects.create(
            username=self.anonymous_login.token,
            password="password",
        )
        self.assertEqual(user.anonymous_login, self.anonymous_login)

    def test_user_get_no_anonymous_login(self):
        """
        Assert that User can not access an AnonymousLogin
        :return:
        """
        user = User.objects.create(username="user", password="password")
        self.assertIsNone(user.anonymous_login)

    def test_anonymous_login_with_cookie_authentication(self):
        """
        Assert that cookie authentication works
        :return:
        """
        # create anonymous login and check if cookie is set
        url = reverse("auth_anonymous-list")
        response = self.client.post(url)
        self.assertEqual(HTTP_201_CREATED, response.status_code)
        self.assertEqual(
            response.cookies["anonymous_token"].value,
            f"Token {response.data['token']}",
        )

        # set cookies and make sure it works
        url = reverse("privatemodel-list")
        self.client.cookies.load({"anonymous_token": f"Token {response.data['token']}"})
        response = self.client.get(url)
        self.assertEqual(HTTP_200_OK, response.status_code)
