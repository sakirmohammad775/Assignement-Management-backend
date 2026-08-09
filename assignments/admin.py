from django.contrib import admin

from .models import Assignment, Submission


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "teacher",
        "class_group",
        "subject",
        "deadline",
        "max_marks",
        "status",
    )

    list_filter = (
        "status",
        "subject",
        "class_group",
    )

    search_fields = (
        "title",
        "description",
    )


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = (
        "assignment",
        "student",
        "status",
        "marks",
        "submitted_at",
    )

    list_filter = (
        "status",
        "assignment",
    )

    search_fields = (
        "student__username",
        "assignment__title",
    )