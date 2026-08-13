from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)

urlpatterns = [
    path("admin/", admin.site.urls),

    # Authentication + Admin
    path(
        "api/auth/",
        include("accounts.urls"),
    ),

    # Assignments + Submissions
    path(
        "api/",
        include("assignments.urls"),
    ),

    # Academics
    path(
        "api/academics/",
        include("academics.urls"),
    ),

    # API Schema
    path(
        "api/schema/",
        SpectacularAPIView.as_view(),
        name="schema",
    ),

    # Swagger
    path(
        "swagger/",
        SpectacularSwaggerView.as_view(
            url_name="schema"
        ),
        name="swagger-ui",
    ),
]