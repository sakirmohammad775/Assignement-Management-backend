from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)
urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "api/auth/",
        include("accounts.urls"),
    ),
    path(
        "api/",
        include("assignments.urls"),
    ),
    path(
        "api/",
        include("academics.urls"),
    ),
    path(
        "api/schema/",
        SpectacularAPIView.as_view(),
        name="schema",
    ),
    path(
        "swagger/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
]
