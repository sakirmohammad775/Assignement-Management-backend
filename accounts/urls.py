from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    AdminUserViewSet,
    LoginView,
    AdminTeacherViewSet,
    AdminStudentViewSet,
    AdminStudentClassView,
)

router = DefaultRouter()

router.register(
    "admin/users",
    AdminUserViewSet,
    basename="admin-users",
)

router.register(
    "admin/teachers",
    AdminTeacherViewSet,
    basename="admin-teachers",
)

router.register(
    "admin/students",
    AdminStudentViewSet,
    basename="admin-students",
)

urlpatterns = [
    path(
        "login/",
        LoginView.as_view(),
        name="login",
    ),

    path(
        "admin/students/<int:student_id>/class/",
        AdminStudentClassView.as_view(),
        name="admin-student-class",
    ),

    path(
        "",
        include(router.urls),
    ),
]