from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ("username", "email", "first_name", "last_name", "is_active", "is_staff")
    fieldsets = UserAdmin.fieldsets + (
        ("Extra info", {"fields": ("middle_name", "gender", "avatar")}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Extra info", {"fields": ("email", "middle_name", "gender", "avatar")}),
    )