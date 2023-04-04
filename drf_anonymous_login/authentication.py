from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework import authentication, exceptions

from .models import AnonymousLogin

AUTH_KEYWORD = "Token"
AUTH_HEADER = "HTTP_X_AUTHORIZATION_ANONYMOUS"


class AnonymousLoginAuthentication(authentication.BaseAuthentication):
    keyword = AUTH_KEYWORD

    def authenticate(self, request):
        auth = request.META.get(AUTH_HEADER, "").split()

        if not auth or auth[0].lower() != self.keyword.lower():
            return None

        if len(auth) == 1:
            msg = _("Invalid token header. No credentials provided.")
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = _("Invalid token header. Token string should not contain spaces.")
            raise exceptions.AuthenticationFailed(msg)

        try:
            anonymous_login = AnonymousLogin.objects.get(token=auth[1])
            if (
                anonymous_login.expiration_datetime
                and anonymous_login.expiration_datetime <= timezone.now()
            ):
                raise exceptions.AuthenticationFailed("Expired authentication token")
        except AnonymousLogin.DoesNotExist:
            raise exceptions.AuthenticationFailed("Invalid authentication token")

        return User(username=anonymous_login.token), None
