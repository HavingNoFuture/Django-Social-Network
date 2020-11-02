from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .forms import UserRegistrationForm, UserEditForm
from .models import Profile


@admin.register(get_user_model())
class CustomUserAdmin(UserAdmin):
    add_form = UserRegistrationForm
    form = UserEditForm
    model = get_user_model()
    list_display = (
        "username",
        "email",
        "is_staff",
        "is_active",
    )
    list_filter = (
        "is_staff",
        "is_active",
    )
    search_fields = ("username", "email")
    ordering = ("-id",)

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("first_name", "middle_name", "last_name", "email")}),
        (
            _("Permissions"),
            {
                "fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions"),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "gender", "phone")
    list_filter = ("gender",)
    search_fields = ("user.username", "user.email")
    ordering = ("-id",)
