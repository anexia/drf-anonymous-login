import re

from rest_framework import (
    filters,
    mixins,
    pagination,
    permissions,
    serializers,
    status,
    viewsets,
)
from rest_framework.response import Response

from drf_anonymous_login.authentication import AnonymousLoginAuthentication
from drf_anonymous_login.models import AnonymousLogin


class AnonymousLoginSerializer(serializers.Serializer):
    pass


class CreateAnonymousLoginViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = AnonymousLoginSerializer
    authentication_classes = ()
    permission_classes = (permissions.AllowAny,)

    @staticmethod
    def extract_request_headers(request):
        regex = re.compile("^HTTP_")
        return dict(
            (regex.sub("", header), value)
            for (header, value) in request.META.items()
            if header.startswith("HTTP_")
        )

    def create(self, request, *args, **kwargs):
        user = AnonymousLogin.objects.create(
            request_data={
                "data": request.data,
                "headers": self.extract_request_headers(request),
            }
        )
        return Response({"token": user.token}, status=status.HTTP_201_CREATED)


class AnonymousLoginAuthenticationModelViewSet(viewsets.ModelViewSet):
    filter_backends = (filters.SearchFilter,)
    authentication_classes = (AnonymousLoginAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = pagination.LimitOffsetPagination
