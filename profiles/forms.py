from django import forms

from profiles.models import Profile


class ProfileEditForm(forms.ModelForm):
    """
    Форма редактирования профиля
    """

    class Meta:
        model = Profile
        fields = ("date_of_birth", "avatar", "github_url", "bio", "phone", "skills", "gender")
