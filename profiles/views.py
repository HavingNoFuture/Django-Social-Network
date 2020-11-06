from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import DetailView
from django.views.generic.base import View

from accounts.forms import UserEditForm
from profiles.forms import ProfileEditForm
from profiles.models import Profile


class ProfileViewMixin:
    """
    Общий миксин для всех вьюх с профилем пользователя.
    """

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({"current_section": "profile"})
        return context


class ProfileView(ProfileViewMixin, DetailView):
    """
    Вывод информации профиля пользователя
    """

    template_name = "profiles/profile.html"
    queryset = Profile.objects.select_related("user").all()

    def get_object(self, queryset=None):
        profile_object = self.queryset.get(user__id=self.request.user.id)
        return profile_object


class ProfileEditView(ProfileViewMixin, LoginRequiredMixin, View):
    """
    Редактирование аккаунта и профиля пользователя
    """

    def get(self, request, *args, **kwargs):
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
        return render(
            request,
            "accounts/edit.html",
            {"user_form": user_form, "profile_form": profile_form, "current_section": "profile"},
        )

    def post(self, request, *args, **kwargs):
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Профиль был успешно обновлен")
        else:
            messages.error(request, "Ошибка при обновлении профиля")
        return render(
            request,
            "accounts/edit.html",
            {"user_form": user_form, "profile_form": profile_form, "current_section": "profile"},
        )
