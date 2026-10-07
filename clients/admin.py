from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class ClientUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Client profile', {'fields': ('avatar', 'birth_date', 'gender')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Client profile', {'fields': ('avatar', 'birth_date', 'gender')}),
    )
