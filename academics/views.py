from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

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


class ClassViewSet(viewsets.ModelViewSet):
    queryset = Class.objects.all()
    serializer_class = ClassSerializer
    permission_classes = [IsAuthenticated]


class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [IsAuthenticated]


class TeacherClassViewSet(viewsets.ModelViewSet):
    queryset = TeacherClass.objects.select_related(
        "teacher",
        "class_group",
    )
    serializer_class = TeacherClassSerializer
    permission_classes = [IsAuthenticated]


class TeacherSubjectViewSet(viewsets.ModelViewSet):
    queryset = TeacherSubject.objects.select_related(
        "teacher",
        "subject",
        "class_group",
    )
    serializer_class = TeacherSubjectSerializer
    permission_classes = [IsAuthenticated]


class StudentClassViewSet(viewsets.ModelViewSet):
    queryset = StudentClass.objects.select_related(
        "student",
        "class_group",
    )
    serializer_class = StudentClassSerializer
    permission_classes = [IsAuthenticated]