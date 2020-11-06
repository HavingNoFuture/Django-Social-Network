from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.views.generic import FormView
from django.views.generic.base import TemplateView, View

from accounts.forms import UserRegistrationForm, UserLoginForm
from accounts.tokens import account_activation_token
from utils.utils import simple_response

User = get_user_model()


class UserLoginView(LoginView):
    """
    Авторизация пользователя по username или email и паролю
    """

    form_class = UserLoginForm


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
