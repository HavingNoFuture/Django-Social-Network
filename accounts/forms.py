from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from accounts.models import Profile
from accounts.tokens import account_activation_token


class UserRegistrationForm(UserCreationForm):
    """
    Форма регистрации пользователя
    """

    class Meta(UserCreationForm):
        model = get_user_model()
        fields = ("email", "password1", "password2")

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
                "user": self.instance,
                "domain": current_site.domain,
                "uid": urlsafe_base64_encode(force_bytes(self.instance.pk)),
                "token": account_activation_token.make_token(self.instance),
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
        fields = ("first_name", "last_name", "email")


class ProfileEditForm(forms.ModelForm):
    """
    Форма редактирования профиля
    """

    class Meta:
        model = Profile
        fields = ("date_of_birth", "photo")
