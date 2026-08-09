from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = (
        "username",
        "email",
        "role",
        "is_active",
    )

    list_filter = (
        "role",
        "is_active",
    )

    fieldsets = UserAdmin.fieldsets + (
        (
            "Role",
            {
                "fields": ("role",),
            },
        ),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            "Role",
            {
                "fields": ("email", "role"),
            },
        ),
    )