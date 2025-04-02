from django.contrib import admin
from apps.accounts.models import User, UserResetPassword
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# Register your models here.

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    add_fieldsets = (
            (
                None,
                {
                    "classes": ("wide",),
                    "fields": ("email", "password1", "password2", "username"),
                },
            ),
        )
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (("Personal info"), {"fields": ("first_name", "last_name", "email" , "phone", "birth",  "photo")}),
        (
            ("Permissions"),
            {
                "fields": (
                    "status",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    list_display = ("username", "email", "first_name", "last_name", "phone", "birth","status", "is_staff")
    list_editable = ("status", )


@admin.register(UserResetPassword)
class UserResetPasswordCodeAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', )
    list_display_links=('id', 'email', )
    