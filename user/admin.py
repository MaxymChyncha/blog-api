from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from user.models import User, PasswordResetToken
from django.contrib.auth.models import Group
from django.utils.translation import gettext as _


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    fieldsets = (
        (None, {"fields": ("email", "username", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "avatar")}),
        (_("Permissions"), {"fields": ("is_active", "is_staff", "is_superuser",
                                       "groups", "user_permissions")}),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "password1", "password2"),
        }),
    )
    list_display = ("email", "first_name", "last_name", "is_staff")
    search_fields = ("email", "first_name", "last_name")
    ordering = ("email",)


@admin.register(PasswordResetToken)
class PasswordResetTokenAdmin(admin.ModelAdmin):
    list_display = ("user", "token", "created_at", "expires_at")
    search_fields = ("user__username", "user__email", "token")
    list_filter = ("created_at", "expires_at")
    ordering = ("-created_at",)


admin.site.unregister(Group)
