from rest_framework import serializers

from .models import (
    Class,
    Subject,
    TeacherClass,
    TeacherSubject,
    StudentClass,
)


class ClassSerializer(serializers.ModelSerializer):
    student_count = serializers.IntegerField(
        source="students.count",
        read_only=True,
    )

    class Meta:
        model = Class
        fields = [
            "id",
            "name",
            "code",
            "student_count",
        ]


class SubjectSerializer(serializers.ModelSerializer):
    teacher_count = serializers.IntegerField(
        source="teacher_assignments.count",
        read_only=True,
    )

    class Meta:
        model = Subject
        fields = [
            "id",
            "name",
            "code",
            "teacher_count",
        ]


class TeacherClassSerializer(serializers.ModelSerializer):
    teacher_name = serializers.CharField(
        source="teacher.username",
        read_only=True,
    )

    class_name = serializers.CharField(
        source="class_group.name",
        read_only=True,
    )

    class Meta:
        model = TeacherClass
        fields = [
            "id",
            "teacher",
            "teacher_name",
            "class_group",
            "class_name",
        ]


class TeacherSubjectSerializer(serializers.ModelSerializer):
    teacher_name = serializers.CharField(
        source="teacher.username",
        read_only=True,
    )

    subject_name = serializers.CharField(
        source="subject.name",
        read_only=True,
    )

    class_name = serializers.CharField(
        source="class_group.name",
        read_only=True,
    )

    class Meta:
        model = TeacherSubject
        fields = [
            "id",
            "teacher",
            "teacher_name",
            "subject",
            "subject_name",
            "class_group",
            "class_name",
        ]


class StudentClassSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(
        source="student.username",
        read_only=True,
    )

    class_name = serializers.CharField(
        source="class_group.name",
        read_only=True,
    )

    class Meta:
        model = StudentClass
        fields = [
            "id",
            "student",
            "student_name",
            "class_group",
            "class_name",
        ]