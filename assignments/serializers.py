from django.utils import timezone
from django.utils import timezone
from rest_framework import serializers
from .models import Assignment,Submission


class AssignmentSerializer(serializers.ModelSerializer):
    teacher_name = serializers.CharField(
        source="teacher.username",
        read_only=True,
    )
    class_name = serializers.CharField(
        source="class_group.name",
        read_only=True,
    )
    subject_name = serializers.CharField(
        source="subject.name",
        read_only=True,
    )

    class Meta:
        model = Assignment
        fields = [
            "id",
            "teacher",
            "teacher_name",
            "class_group",
            "class_name",
            "subject",
            "subject_name",
            "title",
            "description",
            "deadline",
            "max_marks",
            "status",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "teacher",
            "status",
            "created_at",
            "updated_at",
        ]

    def validate(self, attrs):
        request = self.context["request"]

        class_group = attrs.get("class_group")
        subject = attrs.get("subject")

        # Teacher must actually teach this class.
        if not class_group:
            raise serializers.ValidationError({
                "class_group": "Class is required."
            })

        if not subject:
            raise serializers.ValidationError({
                "subject": "Subject is required."
            })

        teaches_class = class_group.teacher_assignments.filter(
            teacher=request.user
        ).exists()

        if not teaches_class:
            raise serializers.ValidationError(
                "You are not assigned to this class."
            )

        teaches_subject = subject.teacher_assignments.filter(
            teacher=request.user,
            class_group=class_group,
        ).exists()

        if not teaches_subject:
            raise serializers.ValidationError(
                "You are not assigned to this subject for this class."
            )

        return attrs
    

class SubmissionSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(
        source="student.username",
        read_only=True,
    )

    assignment_title = serializers.CharField(
        source="assignment.title",
        read_only=True,
    )

    teacher_name = serializers.CharField(
        source="assignment.teacher.username",
        read_only=True,
    )

    class_name = serializers.CharField(
        source="assignment.class_group.name",
        read_only=True,
    )

    subject_name = serializers.CharField(
        source="assignment.subject.name",
        read_only=True,
    )

    max_marks = serializers.IntegerField(
        source="assignment.max_marks",
        read_only=True,
    )

    class Meta:
        model = Submission

        fields = [
            "id",
            "assignment",
            "assignment_title",
            "teacher_name",
            "class_name",
            "subject_name",
            "student",
            "student_name",
            "answer",
            "submitted_at",
            "updated_at",
            "status",
            "marks",
            "feedback",
            "max_marks",
        ]

        read_only_fields = [
            "student",
            "submitted_at",
            "updated_at",
            "status",
            "marks",
            "feedback",
        ]

    def validate_assignment(self, assignment):
        request = self.context["request"]

        # Assignment must be published
        if assignment.status != Assignment.Status.PUBLISHED:
            raise serializers.ValidationError(
                "This assignment is not published."
            )

        # Student must belong to assignment class
        try:
            student_class = request.user.student_class.class_group
        except Exception:
            raise serializers.ValidationError(
                "You are not assigned to a class."
            )

        if student_class != assignment.class_group:
            raise serializers.ValidationError(
                "You cannot submit this assignment."
            )

        # Deadline check
        if timezone.now() > assignment.deadline:
            raise serializers.ValidationError(
                "The submission deadline has passed."
            )

        return assignment
    