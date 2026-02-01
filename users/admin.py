from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ["username", "email", "phone", "is_staff", "is_active", "created_at"]
    list_filter = ["is_staff", "is_active", "created_at"]
    search_fields = ["username", "email", "phone"]
    ordering = ["-created_at"]

    fieldsets = UserAdmin.fieldsets + (
        ("Información Adicional", {"fields": ("phone", "created_at", "updated_at")}),
    )

    readonly_fields = ["created_at", "updated_at"]
