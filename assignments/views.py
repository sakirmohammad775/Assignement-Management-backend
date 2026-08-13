from rest_framework import status, viewsets, serializers
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from accounts.permissions import IsStudent, IsTeacher
from .models import Assignment, Submission
from .serializers import (
    AssignmentSerializer,
    SubmissionSerializer,
)
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.utils import extend_schema, OpenApiParameter

@extend_schema(
    parameters=[
        OpenApiParameter(
            name="id",
            type=int,
            location=OpenApiParameter.PATH,
        )
    ]
)

class AssignmentViewSet(viewsets.ModelViewSet):
    serializer_class = AssignmentSerializer

    def get_permissions(self):
        if self.action in [
            "create",
            "update",
            "partial_update",
            "destroy",
            "publish",
        ]:
            return [IsTeacher()]

        return [IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user

        if user.role == "TEACHER":
            return Assignment.objects.filter(teacher=user).select_related(
                "teacher",
                "class_group",
                "subject",
            )

        if user.role == "STUDENT":
            try:
                student_class = user.student_class.class_group
            except Exception:
                return Assignment.objects.none()

            return Assignment.objects.filter(
                class_group=student_class,
                status=Assignment.Status.PUBLISHED,
            ).select_related(
                "teacher",
                "class_group",
                "subject",
            )

        # Admin can see everything.
        if user.role == "ADMIN":
            return Assignment.objects.all().select_related(
                "teacher",
                "class_group",
                "subject",
            )

        return Assignment.objects.none()

    def perform_create(self, serializer):
        serializer.save(teacher=self.request.user)

    def perform_update(self, serializer):
        assignment = self.get_object()

        if assignment.teacher != self.request.user:
            raise PermissionDenied("You can only modify your own assignments.")

        serializer.save()

    def destroy(self, request, *args, **kwargs):
        assignment = self.get_object()

        if assignment.teacher != request.user:
            return Response(
                {"detail": "You can only delete your own assignments."},
                status=status.HTTP_403_FORBIDDEN,
            )

        assignment.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        methods=["post"],
        permission_classes=[IsTeacher],
    )
    def publish(self, request, pk=None):
        assignment = self.get_object()

        if assignment.teacher != request.user:
            return Response(
                {"detail": "You can only publish your own assignments."},
                status=status.HTTP_403_FORBIDDEN,
            )

        assignment.status = Assignment.Status.PUBLISHED
        assignment.save(update_fields=["status", "updated_at"])

        return Response(
            AssignmentSerializer(
                assignment,
                context={"request": request},
            ).data
        )

    @action(
        detail=True,
        methods=["post"],
        permission_classes=[IsTeacher],
    )
    def draft(self, request, pk=None):
        assignment = self.get_object()

        if assignment.teacher != request.user:
            return Response(
                {"detail": "You can only move your own assignments to draft."},
                status=status.HTTP_403_FORBIDDEN,
            )

        assignment.status = Assignment.Status.DRAFT
        assignment.save(update_fields=["status", "updated_at"])

        return Response(
            AssignmentSerializer(
                assignment,
                context={"request": request},
            ).data
        )

@extend_schema(
    parameters=[
        OpenApiParameter(
            name="id",
            type=int,
            location=OpenApiParameter.PATH,
        )
    ]
)

class SubmissionViewSet(viewsets.ModelViewSet):
    serializer_class = SubmissionSerializer

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update"]:
            return [IsStudent()]

        return [IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user

        if user.role == "STUDENT":
            return Submission.objects.filter(student=user).select_related(
                "assignment",
                "student",
            )

        if user.role == "TEACHER":
            return Submission.objects.filter(assignment__teacher=user).select_related(
                "assignment",
                "student",
            )

        if user.role == "ADMIN":
            return Submission.objects.all().select_related(
                "assignment",
                "student",
            )

        return Submission.objects.none()

    def perform_create(self, serializer):
        assignment = serializer.validated_data["assignment"]

        # Prevent duplicate submission
        if Submission.objects.filter(
            assignment=assignment,
            student=self.request.user,
        ).exists():
            raise serializers.ValidationError(
                "You have already submitted this assignment."
            )

        serializer.save(
            student=self.request.user,
            status=Submission.Status.SUBMITTED,
        )

    def perform_update(self, serializer):
        submission = self.get_object()

        if submission.student != self.request.user:
            raise PermissionDenied("You can only update your own submission.")

        if timezone.now() > submission.assignment.deadline:
            raise serializers.ValidationError("The submission deadline has passed.")

        if submission.status == Submission.Status.GRADED:
            raise serializers.ValidationError("A graded submission cannot be updated.")

        serializer.save()

    @action(
        detail=True,
        methods=["post"],
        permission_classes=[IsTeacher],
    )
    def grade(self, request, pk=None):
        submission = self.get_object()

        if submission.assignment.teacher != request.user:
            return Response(
                {"detail": "You can only grade submissions " "for your assignments."},
                status=status.HTTP_403_FORBIDDEN,
            )

        marks = request.data.get("marks")
        feedback = request.data.get("feedback", "")

        if marks is None:
            return Response(
                {"marks": "Marks are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            marks = int(marks)
        except (TypeError, ValueError):
            return Response(
                {"marks": "Marks must be a number."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if marks < 0:
            return Response(
                {"marks": "Marks cannot be negative."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if marks > submission.assignment.max_marks:
            return Response(
                {
                    "marks": (
                        f"Marks cannot exceed " f"{submission.assignment.max_marks}."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        submission.marks = marks
        submission.feedback = feedback
        submission.status = Submission.Status.GRADED

        submission.save(
            update_fields=[
                "marks",
                "feedback",
                "status",
                "updated_at",
            ]
        )

        return Response(
            SubmissionSerializer(
                submission,
                context={"request": request},
            ).data
        )

    def get_queryset(self):
        user = self.request.user

        if user.role == "ADMIN":
            return Assignment.objects.all().select_related(
                "teacher",
                "class_group",
                "subject",
            )

        if user.role == "TEACHER":
            return Assignment.objects.filter(teacher=user).select_related(
                "teacher",
                "class_group",
                "subject",
            )

        if user.role == "STUDENT":
            try:
                student_class = user.student_class.class_group
            except Exception:
                return Assignment.objects.none()

            return Assignment.objects.filter(
                class_group=student_class,
                status=Assignment.Status.PUBLISHED,
            ).select_related(
                "teacher",
                "class_group",
                "subject",
            )

        return Assignment.objects.none()

    def get_queryset(self):
        user = self.request.user

        if user.role == "STUDENT":
            return Submission.objects.filter(student=user).select_related(
                "assignment",
                "assignment__teacher",
                "assignment__class_group",
                "assignment__subject",
                "student",
            )

        if user.role == "TEACHER":
            return Submission.objects.filter(assignment__teacher=user).select_related(
                "assignment",
                "assignment__teacher",
                "assignment__class_group",
                "assignment__subject",
                "student",
            )

        if user.role == "ADMIN":
            return Submission.objects.all().select_related(
                "assignment",
                "assignment__teacher",
                "assignment__class_group",
                "assignment__subject",
                "student",
            )

        return Submission.objects.none()
