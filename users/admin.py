from .models import MyUser
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseAdmin


class UserAdmin(BaseAdmin):
    list_display = ["email", "username", "is_active", "is_staff", "is_superuser"]
    list_filter = ["is_staff"]
    fieldsets = [
        (None, {"fields": ["email", "password"]}),
        ("Permissions", {"fields": ["is_staff"]}),
    ]

    search_fields = ["email"]
    ordering = ["email"]
    filter_horizontal = []

admin.site.register(MyUser, UserAdmin)
