from rest_framework import viewsets
from drf_spectacular.utils import extend_schema, OpenApiParameter

from .models import (
    Class,
    Subject,
    TeacherClass,
    TeacherSubject,
    StudentClass,
)

from .serializers import (
    ClassSerializer,
    SubjectSerializer,
    TeacherClassSerializer,
    TeacherSubjectSerializer,
    StudentClassSerializer,
)

from accounts.permissions import (
    IsAdmin,
    IsTeacherOrAdmin,
)


from rest_framework.permissions import IsAuthenticated
from accounts.permissions import IsAdmin, IsTeacherOrAdmin


class ClassViewSet(viewsets.ModelViewSet):
    queryset = Class.objects.all().order_by("name")
    serializer_class = ClassSerializer

    def get_permissions(self):
        if self.action in [
            "create",
            "update",
            "partial_update",
            "destroy",
        ]:
            return [IsAdmin()]

        return [IsTeacherOrAdmin()]


class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all().order_by("name")
    serializer_class = SubjectSerializer

    def get_permissions(self):
        if self.action in [
            "create",
            "update",
            "partial_update",
            "destroy",
        ]:
            return [IsAdmin()]

        return [IsTeacherOrAdmin()]

@extend_schema(
    parameters=[
        OpenApiParameter(
            name="id",
            type=int,
            location=OpenApiParameter.PATH,
        )
    ]
)
class TeacherClassViewSet(viewsets.ModelViewSet):
    serializer_class = TeacherClassSerializer
    permission_classes = [IsTeacherOrAdmin]

    def get_queryset(self):
        user = self.request.user

        queryset = TeacherClass.objects.select_related(
            "teacher",
            "class_group",
        )

        # Teacher → only their own classes
        if user.role == "TEACHER":
            return queryset.filter(teacher=user)

        # Admin → all teacher/class assignments
        return queryset


@extend_schema(
    parameters=[
        OpenApiParameter(
            name="id",
            type=int,
            location=OpenApiParameter.PATH,
        )
    ]
)

class TeacherSubjectViewSet(viewsets.ModelViewSet):
    serializer_class = TeacherSubjectSerializer
    permission_classes = [IsTeacherOrAdmin]

    def get_queryset(self):
        user = self.request.user

        queryset = TeacherSubject.objects.select_related(
            "teacher",
            "subject",
            "class_group",
        )

        # Teacher → only their own subjects
        if user.role == "TEACHER":
            return queryset.filter(teacher=user)

        # Admin → all teacher/subject assignments
        return queryset


class StudentClassViewSet(viewsets.ModelViewSet):
    queryset = StudentClass.objects.select_related(
        "student",
        "class_group",
    )
    serializer_class = StudentClassSerializer
    permission_classes = [IsAdmin]
