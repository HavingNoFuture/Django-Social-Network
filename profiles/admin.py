from django.contrib import admin

from profiles.models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "gender", "phone")
    list_filter = ("gender",)
    search_fields = ("user.username", "user.email")
    ordering = ("-id",)
