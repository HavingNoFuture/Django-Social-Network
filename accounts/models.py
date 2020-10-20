from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _

from accounts.managers import AccountManager


class Account(AbstractUser):
    """
    Аккаунт пользователя.
    Основания модель пользователя
    """

    username = None
    email = models.EmailField(_("email address"), unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = AccountManager()

    class Meta:
        verbose_name = "Аккаунт пользователя"
        verbose_name_plural = "Аккаунты пользователей"
        ordering = ("-id",)

    def __str__(self):
        return self.email


class Profile(models.Model):
    """
    Профиль пользователя
    """

    user = models.OneToOneField(
        get_user_model(), verbose_name="Аккаунт", on_delete=models.CASCADE
    )
    date_of_birth = models.DateField("Дата рождения", blank=True, null=True)
    photo = models.ImageField("Аватар", upload_to="users/%Y/%m/%d/", blank=True)

    class Meta:
        verbose_name = "Профиль пользователя"
        verbose_name_plural = "Профили пользователей"
        ordering = ("-id",)

    def __str__(self):
        return f"Профиль пользователя {self.user.email}"


@receiver(post_save, sender=get_user_model())
def update_user_profile(sender, instance, created, **kwargs):
    """
    При сохранении аккаунта привязывает к нему новый профиль
    """
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
