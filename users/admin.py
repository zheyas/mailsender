from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + ((None, {"fields": ("role", "is_blocked")}),)
    # 'username' убираем!
    list_display = ("email", "role", "is_active", "is_blocked", "is_staff")
    list_filter = ("role", "is_active", "is_blocked")
    ordering = ("email",)  # если вдруг будет ordering — только по email

    # Рекомендуется добавить, если вы убрали username в модели:
    search_fields = ("email",)
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "role",
                    "is_blocked",
                    "is_staff",
                    "is_active",
                ),
            },
        ),
    )
