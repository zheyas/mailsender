from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + ((None, {"fields": ("role", "is_blocked")}),)
    list_display = ("username", "email", "role", "is_active", "is_blocked", "is_staff")
    list_filter = ("role", "is_active", "is_blocked")
