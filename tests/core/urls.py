from django.contrib import admin
from django.urls import include, path

from rest_framework import routers

from testapp.views import PrivateModelViewSet, PublicModelViewSet

from drf_anonymous_login.views import CreateAnonymousLoginViewSet

router = routers.DefaultRouter()
# app routes
router.register(r"public_models", PublicModelViewSet)
router.register(r"private_models", PrivateModelViewSet)

# anonymous login route
router.register(
    r"auth_anonymous",
    CreateAnonymousLoginViewSet,
    basename="auth_anonymous",
)

urlpatterns = [path("admin/", admin.site.urls), path("api/", include(router.urls))]
