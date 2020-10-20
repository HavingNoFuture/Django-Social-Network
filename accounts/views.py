from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic import CreateView, FormView, UpdateView
from django.views.generic.base import TemplateView, View

from accounts.forms import UserRegistrationForm, UserEditForm, ProfileEditForm
from accounts.tokens import account_activation_token
from utils.utils import simple_response

User = get_user_model()


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({"current_section": "dashboard"})
        return context


class RegisterView(FormView):
    """
    Регистрация пользователя
    """

    template_name = "accounts/register.html"
    form_class = UserRegistrationForm

    def form_valid(self, form):
        user_form = UserRegistrationForm(self.request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.is_active = False
            new_user.save()

            user_form.send_activation_email(self.request)
        return simple_response(
            self.request,
            "Мы выслали ссылку для активации аккаунта. Проверьте свою почту.",
        )


class AccountActivationView(View):
    """
    Активация аккаунта
    """

    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            return render(request, "accounts/register_done.html", {"new_user": user})
        else:
            return simple_response(request, "Неверная ссылка активации аккаунта!")


class AccountEditView(LoginRequiredMixin, View):
    """
    Редактирование аккаунта и профиля пользователя
    """

    def get(self, request, *args, **kwargs):
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
        return render(
            request,
            "accounts/edit.html",
            {"user_form": user_form, "profile_form": profile_form},
        )

    def post(self, request, *args, **kwargs):
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(
            instance=request.user.profile, data=request.POST, files=request.FILES
        )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Профиль был успешно обновлен")
        else:
            messages.error(request, "Ошибка при обновлении профиля")
        return render(
            request,
            "accounts/edit.html",
            {"user_form": user_form, "profile_form": profile_form},
        )
