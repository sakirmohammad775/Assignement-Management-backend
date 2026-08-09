from django.contrib import admin

# Register your models here.
from django.contrib import admin

from .models import (
    Class,
    Subject,
    TeacherClass,
    TeacherSubject,
    StudentClass,
)


@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ("name", "code")
    search_fields = ("name", "code")


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ("name", "code")
    search_fields = ("name", "code")


@admin.register(TeacherClass)
class TeacherClassAdmin(admin.ModelAdmin):
    list_display = ("teacher", "class_group")
    list_filter = ("class_group",)


@admin.register(TeacherSubject)
class TeacherSubjectAdmin(admin.ModelAdmin):
    list_display = ("teacher", "subject", "class_group")
    list_filter = ("subject", "class_group")


@admin.register(StudentClass)
class StudentClassAdmin(admin.ModelAdmin):
    list_display = ("student", "class_group")
    list_filter = ("class_group",)