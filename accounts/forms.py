from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.translation import ugettext_lazy as _

from accounts.tokens import account_activation_token


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label="Email или логин", widget=forms.TextInput(attrs={"autofocus": True}))

    error_messages = {
        "invalid_login": _(
            "Пожалуйста, введите правильную пару Email/имя пользователя и пароль. "
            "Оба поля могут быть чувствительны к регистру."
        ),
        "inactive": _("This account is inactive."),
    }


class UserRegistrationForm(UserCreationForm):
    """
    Форма регистрации пользователя
    """

    class Meta(UserCreationForm):
        model = get_user_model()
        fields = ("email", "username", "password1", "password2")

    def send_activation_email(self, request) -> None:
        """
        Отправляет пользователю email c ссылкой на активацию аккаунта
        :return:
        """
        current_site = get_current_site(request)
        subject = "Завершение активации на Django Social Network"
        message = render_to_string(
            "accounts/account_activation_email.html",
            {
                "user": self.instance.username,
                "domain": current_site.domain,
                "uid": urlsafe_base64_encode(force_bytes(self.instance.pk)),
                "token": account_activation_token.make_token(self.instance.username),
            },
        )
        self.instance.email_user(subject, message)


class UserEditForm(UserChangeForm):
    """
    Форма редактирования аккаунта
    """

    password = None

    class Meta:
        model = get_user_model()
        fields = ("first_name", "middle_name", "last_name", "email")
